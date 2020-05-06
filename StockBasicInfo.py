import baostock as bs
import pandas as pd


def result_to_csv(filename, result):
    result.to_csv("D:\\{}.csv".format(filename), encoding="gbk", index=False)


class Stock():
    def __init__(self):
        self.bs = bs
        lg = self.bs.login()
        print('login respond error_code:{}, error_msg:{}',lg.error_code, lg.error_msg)

    def __del__(self):
        self.bs.logout()

    def get_stock_list(self):
        rs = self.bs.query_all_stock(day="2017-06-30")
        print('query_all_stock respond error_code:{}, error_msg{}:', rs.error_code, rs.error_msg)
        self.all_stock = []
        while (rs.error_code == '0') & rs.next():
            data = [rs.get_row_data()[0], rs.get_row_data()[2]]
            self.all_stock.append(data)
        result = pd.DataFrame(self.all_stock, columns=["股票代码", "股票名称"])
        return result

    def get_cash_flow(self, code, year, quarter):
        rs_cash_flow = self.bs.query_cash_flow_data(code=code, year=year, quarter=quarter)
        while (rs_cash_flow.error_code == '0') & rs_cash_flow.next():
            return rs_cash_flow.get_row_data()[3]

    def get_all_cash_flow(self, start_year, end_year):
        all_data = []
        for stock in self.all_stock:
            data = {
                'stock_code' : stock
            }
            for i in range(start_year, end_year):
                for j in range(1,5):
                    data["{}_{}".format(i, j)] = self.get_cash_flow(stock, i, j)
            all_data.append(data)
        result = pd.DataFrame(all_data)
        return result


stock = Stock()
result_to_csv("test", stock.get_stock_list())