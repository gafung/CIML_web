import numpy as np
from flask import Flask, send_from_directory, render_template, jsonify, request
from flask_cors import CORS
from keras.models import load_model
from random import randint
app = Flask(__name__,
            static_folder='ciml-client/build/static',
            template_folder='ciml-client/build')
CORS(app)

def get_input_from_args(args):
    side = 1.0 if args.get('side') == "Buy" else 0.0
    return_t5 = float(args.get('return_t5'))
    return_t30 = float(args.get('return_t30'))
    vol_sh_out_pct = float(args.get('vol_sh_out_pct'))
    stake_pct_chg = float(args.get('stake_pct_chg'))
    tran_value = float(args.get('tran_value'))
    mkt_cap = float(args.get('mkt_cap'))
    prev_tran_num = float(args.get('prev_tran_num'))
    hit_rate_5d = float(args.get('hit_rate_5d'))
    hit_rate_30d = float(args.get('hit_rate_30d'))
    hit_rate_90d = float(args.get('hit_rate_90d'))
    return np.array([[side, return_t5, return_t30, vol_sh_out_pct, stake_pct_chg, tran_value, mkt_cap,
                prev_tran_num, hit_rate_5d, hit_rate_30d, hit_rate_90d]])


@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/svm')
def support_vector_machine():
    kernel = request.args.get("kernal")

    X_test, X_train, y_test_30d, y_test_5d, y_test_90d, y_train_30d, y_train_5d, y_train_90d = get_data()

    from sklearn.svm import SVC
    # clf = SVC(kernel=kernal)
    # clf.fit(X_train, y_train_5d)

    import pickle
    # for krnl in ['linear', 'poly', 'sigmoid']:
    #     clf = SVC(kernel=krnl)
    #     clf.fit(X_train, y_train_5d)

    #     pickle.dump(clf, open('SVM_{}.pickle'.format(krnl), "wb"))


    clf = pickle.load(open('SVM_{}.pickle'.format(kernel), "rb"))

    res = clf.predict(get_input_from_args(request.args))

    return jsonify(result='Y' if res[0] > 0.5 else 'N')

@app.route('/dnn')
def neural_network():
    model = load_model('NeuralNetwork_5d_scale3_2HiddenLayer.h5')
    X_test, X_train, y_test_30d, y_test_5d, y_test_90d, y_train_30d, y_train_5d, y_train_90d = get_data(
        negative_label_as_zero=True)
    # scores = model.evaluate(X_train, y_train_5d)
    # res = ""
    # res += "[Train] %s: %.2f%%" % (model.metrics_names[1], scores[1] * 100)

    # scores = model.evaluate(X_test, y_test_5d)
    # res += "[Test] %s: %.2f%%" % (model.metrics_names[1], scores[1] * 100)
    res = model.predict(get_input_from_args(request.args))
    return jsonify(result='Y' if res[0] > 0.5 else 'N')


@app.route('/knn')
def knn():
    k = int(request.args.get("k"))

    X_test, X_train, y_test_30d, y_test_5d, y_test_90d, y_train_30d, y_train_5d, y_train_90d = get_data()


    ## Import the Classifier.
    from sklearn.neighbors import KNeighborsClassifier
    ## Instantiate the model with 5 neighbors.
    # knn = KNeighborsClassifier(n_neighbors=37)
    knn = KNeighborsClassifier(n_neighbors=k)
    ## Fit the model on the training data.
    # res = ""
    knn.fit(X_train, y_train_5d)
    # res += 'KNN score of 5d: {}'.format(round(knn.score(X_test, y_test_5d) * 100, 2))
    # knn.fit(X_train, y_train_30d)
    # res += 'KNN score of 30d: {}'.format(round(knn.score(X_test, y_test_30d) * 100, 2))
    # knn.fit(X_train, y_train_90d)
    # res += 'KNN score of 90d: {}'.format(round(knn.score(X_test, y_test_90d) * 100, 2))
    res = knn.predict(get_input_from_args(request.args))
    return jsonify(result='Y' if res[0]>0.5 else 'N')

@app.route('/random_data')
def random_data():
    X_test, X_train, y_test_30d, y_test_5d, y_test_90d, y_train_30d, y_train_5d, y_train_90d = get_data()
    idx = randint(0, len(X_test)-1)
    return jsonify(X_test.iloc[idx].to_dict())

def get_data(negative_label_as_zero=False):
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

    if negative_label_as_zero:
        insider['return_5d'] = insider['return_5d'].replace(-1, 0)
        insider['return_30d'] = insider['return_30d'].replace(-1, 0)
        insider['return_90d'] = insider['return_90d'].replace(-1, 0)

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
