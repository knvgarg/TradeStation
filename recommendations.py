from sentiment import get_predictions
from lstm import percent_change_dic
import operator, pickle
import numpy


def get_recommendations():
    sentiment_pred = get_predictions()
    lstm_pred = percent_change_dic()

    recommeds = {}

    for key in sentiment_pred.keys():
        if sentiment_pred[key] < 0:
            recommeds[key] = sentiment_pred[key] + lstm_pred[key]
        else:
            recommeds[key] = lstm_pred[key]

    sorted_d = dict(sorted(recommeds.items(), key=operator.itemgetter(1), reverse=True))

    final_dic = {}

    for obj in sorted_d:
        final_dic[obj] = round(lstm_pred[obj][0][0], 2)
        print(obj, final_dic[obj])

    open_file = open("dictionary.pkl", "wb")
    pickle.dump(final_dic, open_file)
    open_file.close()


# get_recommendations()
