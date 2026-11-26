from pathlib import Path
import unittest
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
class SalesDatasetTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.df=pd.read_csv(ROOT/"data"/"sales_data.csv",parse_dates=["order_date"])
    def test_rows_and_unique_orders(self):
        self.assertEqual(len(self.df),5000)
        self.assertTrue(self.df.order_id.is_unique)
    def test_required_values(self):
        self.assertFalse(self.df[["order_date","customer_id","product_name","revenue","profit"]].isna().any().any())
    def test_business_rules(self):
        self.assertTrue((self.df.quantity>0).all())
        self.assertTrue(self.df.discount_pct.between(0,1).all())
        self.assertTrue((self.df.revenue>=0).all())
    def test_profit_reconciliation(self):
        self.assertTrue(((self.df.revenue-self.df.cost-self.df.profit).abs()<0.011).all())
if __name__=="__main__": unittest.main()
