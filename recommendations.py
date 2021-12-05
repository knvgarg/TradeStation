from sentiment import get_predictions
from lstm import percent_change_dic
import operator, pickle
import numpy


def get_recommendations():
    sentiment_pred = get_predictions()
    lstm_pred = percent_change_dic()

    recommeds = {}

    for key in sentiment_pred.keys():
        recommeds[key] = sentiment_pred[key] + lstm_pred[key]

    sorted_d = dict(sorted(recommeds.items(), key=operator.itemgetter(1), reverse=True))

    # open_file = open("recom.pkl", "wb")
    # pickle.dump(sorted_d, open_file)
    # open_file.close()

    # pickle_file = open("dictionary.pkl", "rb")
    # sorted_d = pickle.load(pickle_file)
    # pickle_file.close()

    # for obj in sorted_d:
    #     sorted_d[obj] = round(sorted_d[obj][0][0], 2)
    #     print(obj, sorted_d[obj])

    final_dic = {}

    for obj in sorted_d:
        final_dic[obj] = round(lstm_pred[obj][0][0], 2)
        print(obj, final_dic[obj])

    open_file = open("dictionary.pkl", "wb")
    pickle.dump(final_dic, open_file)
    open_file.close()


# get_recommendations()
