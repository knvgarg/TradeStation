from lstm import retrain_model, update_dataset
from soup import refresh_prices, refresh_database
from recommendations import get_recommendations


##### after market closes ########
# refresh_database()
# update_dataset()

##### before market opens #######
# get_recommendations()
# refresh_database()


###### every weekend #########
# retrain_model()
