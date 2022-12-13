import sqlite3
from flask import render_template, request, redirect, make_response
from flask import Flask
import json

app = Flask(__name__)


@app.route('/api', methods=['GET', 'POST'])
def api():
    if request.method == 'GET':

        connection = sqlite3.connect('stankin.db')
        cursor = connection.cursor()

        if request.args['target'] == 'account':
            res = cursor.execute(
                f"SELECT name, coins, trash_count, oders FROM users_info WHERE id_telegramm = {request.args['id']}")
            res = res.fetchall()
            connection.close()
            return res
        elif request.args['target'] == 'ids':
            res = cursor.execute("SELECT id_telegramm FROM users_info")
            res = res.fetchall()
            connection.close()
            return res
        elif request.args['target'] == 'reg':
            cursor.execute('INSERT INTO users_info (name, coins, trash_count, oders, id_telegramm) VALUES ("{0}", 0, 0, 0, "{1}");'.format(request.args['username'], request.args['id']))
            cursor.execute('INSERT INTO users_goods (telegramm_id, bear, paper, hoodie, cap) VALUES ({0}, 0, 0, 0, 0);'.format(request.args['id']))
            connection.commit()
            connection.close()
            return 'ok'
        elif request.args['target'] == 'buy':
            good = cursor.execute('SELECT {1} FROM users_goods WHERE telegramm_id={0}'.format(request.args['id'], request.args['good']))
            good = good.fetchall()[0][0]
            connection.commit()
            coins = cursor.execute('SELECT coins FROM users_info WHERE id_telegramm={0}'.format(request.args['id']))
            coins = coins.fetchall()[0][0]
            connection.commit()

            if int(coins) >= int(request.args['cost']):
                cursor.execute('UPDATE users_goods SET {0} = {1}'.format(request.args['good'], int(good) + 1))
                cursor.execute('UPDATE users_info SET coins = {1} WHERE id_telegramm={0}'.format(request.args['id'], int(coins) - int(request.args['cost'])))
                connection.commit()
                connection.close()
                return 'ok'
            else:
                connection.close()
                return 'nenmoney'
        elif request.args['target'] == 'goods':
            res = cursor.execute('SELECT * FROM users_goods WHERE telegramm_id={0}'.format(request.args['id'])).fetchall()
            return res
        elif request.args['target'] == 'automate':
            res = cursor.execute(
                f"SELECT trash_counter, machine_full FROM machines WHERE id = {request.args['auto_id']}")
            res = res.fetchall()
            connection.commit()
            connection.close()
            return res
        elif request.args['target'] == 'collect':
            res = cursor.execute(
                f"SELECT trash_count FROM users_info WHERE id_telegramm = {request.args['id']}")
            coins = cursor.execute(
                f"SELECT coins FROM users_info WHERE id_telegramm = {request.args['id']}")
            res_mach = cursor.execute(
                f"SELECT machine_full FROM machines WHERE id = {request.args['mach_id']}")
            res = int(res.fetchall()[0])
            if request.args['trash'] == 'paper':
                coins = int(coins.fetchall()[0]) + 10 * int(request.args['mass'])
            elif request.args['trash'] == 'pastic':
                coins = int(coins.fetchall()[0]) + 15 * int(request.args['mass'])
            elif request.args['trash'] == 'glass':
                coins = int(coins.fetchall()[0]) + 20 * int(request.args['mass'])
            res_mach = int(res_mach.fetchall()[0])
            res += int(request.args['mass'])
            res_mach += int(request.args['mass'])
            cursor.execute(
                'UPDATE users_info SET trash_count={0} WHERE id_telegramm={1};'.format(res, request.args['id']))
            cursor.execute(
                'UPDATE users_info SET coins={0} WHERE id_telegramm={1};'.format(coins, request.args['id']))
            cursor.execute(
                'UPDATE machines SET machine_full={0} WHERE id = {1};'.format(res_mach, request.args['mach_id']))
            connection.commit()
            connection.close()
        elif request.args['target'] == 'quest':
            if request.args['first_time'] == 1:
                cursor.execute(
                    'UPDATE users_info SET first_time=1 WHERE id = {0};'.format(request.args['id']))
            elif request.args['10kg'] == 1:
                cursor.execute(
                    'UPDATE users_info SET 10kg=1 WHERE id = {0};'.format(request.args['id']))
            elif request.args['100kg'] == 1:
                cursor.execute(
                    'UPDATE users_info SET 100kg=1 WHERE id = {0};'.format(request.args['id']))
app.run()
