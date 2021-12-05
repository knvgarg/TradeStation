from lstm import retrain_model, update_dataset
from soup import refresh_prices
from recommendations import get_recommendations


##### after market closes ########
# refresh_prices()
update_dataset()

##### before market opens #######
# get_recommendations()
# refresh_prices()


###### after 10 days #########
# retrain_model()
