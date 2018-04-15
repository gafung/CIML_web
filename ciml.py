from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/a')
def a():
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

    # Splitting test data into two parts
    X_test1 = X_test[:8620]
    X_test2 = X_test[-8620:]
    y_test_90d1 = y_test_90d[:8620]
    y_test_90d2 = y_test_90d[-8620:]

    ## Import the Classifier.
    from sklearn.neighbors import KNeighborsClassifier
    ## Instantiate the model with 5 neighbors.
    knn = KNeighborsClassifier(n_neighbors=37)
    ## Fit the model on the training data.
    knn.fit(X_train, y_train_5d)
    print('KNN score of 5d:', round(knn.score(X_test, y_test_5d) * 100, 2))
    knn.fit(X_train, y_train_30d)
    print('KNN score of 30d:', round(knn.score(X_test, y_test_30d) * 100, 2))
    knn.fit(X_train, y_train_90d)
    print('KNN score of 90d:', round(knn.score(X_test, y_test_90d) * 100, 2))
    print('KNN score of 90d (test1):', round(knn.score(X_test1, y_test_90d1) * 100, 2))
    print('KNN score of 90d (test2):', round(knn.score(X_test2, y_test_90d2) * 100, 2))


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
