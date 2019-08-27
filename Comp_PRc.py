
from telegram import KeyboardButton, ReplyKeyboardMarkup
import public_api as public_api
from binance.client import Client
from telegram import Bot
from telegram.ext import Updater, CommandHandler, ConversationHandler,MessageHandler, Filters
import time
import re
import ccxt
import copy
import threading
from datetime import datetime, timedelta

api = public_api.PublicApi('public_api.ini')
client = Client('Some_Token', 'Some_Token')
bot = Bot(token='Some_Token')
triger = True
date = range(1)
var_for_time = {}


class Tbot(object):

    def __init__(self):
        try:
            self.dics = ['Exmo', 'Binance', 'Bitfinex']
            self.updater = Updater('Some_Token', use_context=True)
            self.dp = self.updater.dispatcher
            self.dp.add_handler(CommandHandler('help', self.help))
            self.dp.add_handler(CommandHandler('start', self.start))
            self.dp.add_handler(CommandHandler('veiw_settings', self.veiw_settings))
            self.dp.add_handler(CommandHandler('reopen', self.reopen))
            self.dp.add_handler(CommandHandler('stop', self.stop))
            self.dp.add_handler(ConversationHandler(entry_points=[CommandHandler('launch', self.launch)],
                                                    states={date: [MessageHandler(Filters.text, self.run)]},
                                                    fallbacks=[CommandHandler('cancel', self.cancel)], allow_reentry = True)
                                )
        except:

            print('problem with class initialization')


    def cancel(self,udpate,context):
        bot.sendMessage(chat_id=udpate.message.chat_id,text=':(')


    def start(self,update, context):
        print('start')
        try:
            kb = [[KeyboardButton('/launch')],
                  [KeyboardButton('/veiw_settings')],
                  [KeyboardButton('/help')],
                  [KeyboardButton('/stop')],
                  [KeyboardButton('/reopen')]]
        except:
            print('keyboard problem')
        try:
            kb_markup = ReplyKeyboardMarkup(kb)
        except:
            print('init keyboard problem')

        bot.send_message(chat_id=update.message.chat_id,
                         text='Chose command',
                         reply_markup=kb_markup)


    def main(self):
        self.updater.start_polling()
        self.updater.idle()

    def checking_and_activate(self,dic, update, context):
        dictafone = self.dics
        intersection = list(set(dic.keys()) & set(dictafone))
        if intersection:
            try:
                my_thred_while = threading.Thread(target=self.activate_while, name = 'second',args= (dic,intersection,update,context,))
                my_thred_while.start()
            except:
                print('problem')

        else:
            bot.sendMessage(chat_id=update.message.chat_id,
                            text='Нет совпадений по названию бирж, для информации наберите /help')



    def activate_while(self,dic,intersection,update,context):
        global triger
        while triger:
            self.transforming_user_dic(dic, intersection, update, context)
            time.sleep(1)


    def transforming_user_dic(self, dic, inter,update, context):
        user_dic = copy.deepcopy(dict(dic))

        for exch in inter:
            try:
                exchange_bin = ccxt.binance()
                exchange_exm = ccxt.exmo()
                exchange_bifin = ccxt.bitfinex()
                exchanges = {'Exmo': exchange_exm.fetchTickers(), 'Binance': exchange_bin.fetchTickers(), 'Bitfinex': exchange_bifin.fetchTickers()}
                api_pairs = exchanges[exch]
                user_pairs = user_dic[exch]
            except:
                print('проблемы с вызовом api')
                self.checking_and_activate(user_dic, update, context)


            intersection = list(set(api_pairs.keys()) & set(user_pairs.keys()))
            for key in intersection:
                t = list(user_pairs[key])
                if len(t) < 3:
                    t.append(api_pairs[key]['bid'])
                    t.append(api_pairs[key]['ask'])
                else:
                    print(api_pairs[key]['bid'])
                    print(api_pairs[key]['ask'])
                    t[2] == api_pairs[key]['bid']
                    t[3] == api_pairs[key]['ask']
                user_pairs[key] = t
            user_dic[exch] = user_pairs
        try:
            self.compare_bid_ask(user_dic, update, context)
        except:
            print('something wrong with compare bid_ask function')

    def compare_bid_ask(self,  user_dic, update, context):
        print('compare_bid_ask', user_dic)
        global var_for_time
        arr = api.get_prices()
        bitqi_dic = {}
        for i in arr:
            for k in i.items():
                if k[0] == 'marketName':
                    bitqi_dic[k[1]] = i

        for exch_name in user_dic.keys():
            dict_pairs = user_dic[exch_name]
            for i in dict_pairs.keys():
                if 'USDT' in i:
                    key = i.replace('USDT', 'USD')
                    dict_pairs[key] = dict_pairs.pop(i)

            dict_pairs = user_dic[exch_name]
            intersection = list(set(dict_pairs.keys()) & set(bitqi_dic.keys()))
            if intersection:
                for pair in intersection:
                    stri = (exch_name + pair)
                    print('СРАВНИМ', datetime.now(), 'and', var_for_time)
                    if stri in var_for_time and var_for_time[stri] >     datetime.now():
                        print('pass')
                        pass
                    else:
                        print('elsik')
                        try:
                            prc = dict_pairs[pair][1]
                            percent = float(dict_pairs[pair][1])

                            bid_bitqi = float(bitqi_dic[pair]['bid'])
                            ask_bitqi = float(bitqi_dic[pair]['ask'])

                            bid_exch  = float(dict_pairs[pair][2])
                            ask_exch = float(dict_pairs[pair][3])
                        except:
                            print('float problem')


                        if dict_pairs[pair][0] == 'prc':
                            print('checking with percent:', dict_pairs[pair][1])
                            if bid_exch > bid_bitqi:
                                diff_bid = ((bid_exch-bid_bitqi)/bid_bitqi) * 100
                            else:
                                diff_bid = ((bid_bitqi - bid_exch) / bid_bitqi) * 100

                            if ask_exch >= ask_bitqi:
                                diff_ask = ((ask_exch - ask_bitqi) / ask_bitqi) * 100
                            else:
                                diff_ask = ((ask_bitqi - ask_exch) / ask_bitqi) * 100

                        if dict_pairs[pair][0] == 'val':
                            print('checking with value:', dict_pairs[pair][1])
                            if bid_exch > bid_bitqi:
                                diff_bid = bid_exch - bid_bitqi
                            else:
                                diff_bid = bid_bitqi - bid_exch
                            diff_ask = ask_exch - ask_bitqi

                            if ask_exch >= ask_bitqi:
                                diff_ask = ask_exch - ask_bitqi
                            else:
                                diff_ask = ask_bitqi - ask_exch


                        if diff_bid >= percent or diff_ask >= percent:
                            try:
                                bot.sendMessage(chat_id=update.message.chat_id,
                                            text= str(exch_name) + "\nвалютная пара: \n" + str(pair) + "\nразница между bid или ask price больше "
                                                 + str(prc) + ", цена на битках bid - \n" + str(bid_bitqi)
                                                 +"\nцена на другой бирже -\n" + str(bid_exch) + "\nРазница цен - " + str(diff_bid)
                                                 + ", цена на битках ask - \n" + str(ask_bitqi)
                                                 + "\nцена на другой бирже -\n" + str(ask_exch) + "\nРазница цен - " + str(diff_ask))


                                kastil = (exch_name + pair)
                                var_for_time[kastil] = datetime.now() + timedelta(minutes = 5)
                                print('time_var',var_for_time)

                            except:
                                print('Something wrong with sending message about bid')

            else:
                bot.sendMessage(chat_id = update.message.chat_id,
                                  text='Нет совпадений по названию валютных пар, для информации наберите /help')
                self.stop()



    def launch(self, update, context):
        print('launchit')
        update.message.reply_text("Пожалуйста введите свои данные как показано в следующем примере"
                                  "\nпример ввода:"
                                  "\nExmo(BTC/USDT:prc=3,ETH/BTC:prc=1); Binance(BTC/USDT:prc=3,ETH/BTC:val=0.00000003)")
        try:
            return date
        except:
            print('wierd')


    def run(self, update, context):
        print('im running')

        global triger
        triger = True
        value = update.message.text
        f = open('value.txt','w')
        f.write(value)

        s = value.replace(' ', '')
        first_share = re.split(r';', s)
        dic = {}
        for i in first_share:
            for_dict = i.split('(')
            dic[for_dict[0]] = for_dict[1].replace(')', '')

        for i in dic.keys():
            dic[i] = dic[i].split(',')

        for i in dic.keys():
            so = dic[i]
            yt = {}
            for k in so:
                p = k.split(':')
                yt[p[0]] = p[1]
            dic[i] = yt

        for i in dic.keys():
            pair = dic[i]
            for k in pair.keys():
                pair[k] = pair[k].split('=')

        bot.sendMessage(chat_id=update.message.chat_id,
                    text="Данные приняты, словарь данных выглядит следующим образом" + str(dic))
        ConversationHandler.END
        try:
            self.checking_and_activate(dic, update, context)
        except:
            print('trouble with checking_and_activate')


    def help(self,update, context):
         bot.sendMessage(chat_id=update.message.chat_id,
                        text="Вы воспользовались командой /help \nДля ввода параметров бирж воспользуйтесь командой /launch и следующей синтаксической конструкцией:\n"
                             "название_биржы (валютная_пара:prc_или_val=процент_сравнения, другая_валютная_пара...);...\n"
                             "пример ввода:\n /launch Exmo(BTC/USDT:prc=3,ETH/BTC:prc=1); Binance(BTC/USDT:prc=3,ETH/BTC:val=0.00000003)\nОбратите внимание на то, что список бирж, на которых доступно"
                             " сравнение на данный момент ограничен такими биржами как Exmo,Binance и Bitfinex.\nПожалуйста, старайтесь избегать ошибок при вводе параметров\n "
                             "Для прекращения работы программы воспользуйтесь командой /stop.")


    def veiw_settings(self, update, context):
        f = open('value.txt')
        strin = f.read()
        bot.sendMessage(chat_id=update.message.chat_id,
                        text=strin)


    def reopen(self, update, context):
        global triger
        self.stop(update,context)
        triger = True
        f = open('value.txt')
        dic = f
        print(dic)
        self.checking_and_activate(dic, update, context)



    def stop(self,update,context):
        bot.sendMessage(chat_id=update.message.chat_id,
                        text="Im stopped")
        global triger
        triger = False
        self.cancel(update,context)


if __name__ == '__main__':
    TB = Tbot()
    thred = threading.Thread(target=TB.main(), name='FIRST')
    thred.start()