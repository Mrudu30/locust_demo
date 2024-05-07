import pymysql.cursors
import pymysql

class twincity_info:
    def connect():
        connection =  pymysql.connect(host="192.168.1.184", user="root", password="", database="twincitiesautoauctions", charset='utf8mb4')
        return connection.cursor(pymysql.cursors.DictCursor)

    def get_current_bid(id):
        cursor = twincity_info.connect()
        try:
            # print(cursor.mogrify("SELECT id,user_id,bid_amount FROM bids where inventory_id = %s  order by bid_amount DESC,created_at ASC LIMIT 1 ", (id,)))
            cursor.execute("SELECT id,user_id,bid_amount FROM bids where inventory_id = %s  order by bid_amount DESC,created_at ASC LIMIT 1 ", (id,))
            result = cursor.fetchone()
            # print(result)
            return result
        except:
            print("except get_current_bid")
            return ()
        finally:
            cursor.close()

    def get_winning_user(invent_id):
        cursor = twincity_info.connect( )
        try:
            cursor.execute("SELECT winner_id FROM inventory WHERE id=%s",(invent_id))
            result = cursor.fetchone()
            print(result)
            return result
        except Exception as e:
            print(e)
            return()
        finally:
            cursor.close()

    # def fetch_user_info():
    #     cursor = self.connect()
    #     try:
    #         cursor.execute("SELECT * FROM manage_customer WHERE ")
