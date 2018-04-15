from flask import Flask
from keras.models import load_model
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/nn')
def neural_network():
    model = load_model('NeuralNetwork_5d_scale3_2HiddenLayer.h5')
    X_test, X_train, y_test_30d, y_test_5d, y_test_90d, y_train_30d, y_train_5d, y_train_90d = get_data()
    scores = model.evaluate(X_train, y_train_5d)
    res = ""
    res += "[Train] %s: %.2f%%" % (model.metrics_names[1], scores[1] * 100)

    scores = model.evaluate(X_test, y_test_5d)
    res += "[Test] %s: %.2f%%" % (model.metrics_names[1], scores[1] * 100)
    return res


@app.route('/knn')
def knn():
    X_test, X_train, y_test_30d, y_test_5d, y_test_90d, y_train_30d, y_train_5d, y_train_90d = get_data()


    ## Import the Classifier.
    from sklearn.neighbors import KNeighborsClassifier
    ## Instantiate the model with 5 neighbors.
    knn = KNeighborsClassifier(n_neighbors=37)
    ## Fit the model on the training data.
    res = ""
    knn.fit(X_train, y_train_5d)
    res += 'KNN score of 5d: {}'.format(round(knn.score(X_test, y_test_5d) * 100, 2))
    knn.fit(X_train, y_train_30d)
    res += 'KNN score of 30d: {}'.format(round(knn.score(X_test, y_test_30d) * 100, 2))
    knn.fit(X_train, y_train_90d)
    res += 'KNN score of 90d: {}'.format(round(knn.score(X_test, y_test_90d) * 100, 2))
    return res


def get_data():
    import pandas as pd
    url = "data_v3.csv"
    insider = pd.read_csv(url, header=0)
    print(insider.shape)
    row_num = insider['side'].count() + 1
    train_num = int(row_num / 3 * 2)
    test_num = -1 * int(row_num / 3)
    col_list = ['side', 'return_t5', "return_t30", "vol_sh_out_pct", "stake_pct_chg", "tran_value", "mkt_cap",
                "prev_tran_num", "hit_rate_5d", "hit_rate_30d", "hit_rate_90d"]

    # Apply Min / Max Scaling
    def scaler(col_name):
        insider[col_name] = (insider[col_name] - insider[col_name].min()) / (
            insider[col_name].max() - insider[col_name].min())

    scaler_list = ['side', 'return_t5', "return_t30", "vol_sh_out_pct", "stake_pct_chg", "tran_value", "mkt_cap",
                   "prev_tran_num", "hit_rate_5d", "hit_rate_30d", "hit_rate_90d"]
    for i in scaler_list:
        scaler(i)
    X_train = insider[col_list][:train_num]
    y_train_5d = insider.return_5d[:train_num]
    y_train_30d = insider.return_30d[:train_num]
    y_train_90d = insider.return_90d[:train_num]
    X_test = insider[col_list][test_num:]
    y_test_5d = insider.return_5d[test_num:]
    y_test_30d = insider.return_30d[test_num:]
    y_test_90d = insider.return_90d[test_num:]
    return X_test, X_train, y_test_30d, y_test_5d, y_test_90d, y_train_30d, y_train_5d, y_train_90d


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
