import mlflow
import catboost
import mlflow.catboost
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    roc_auc_score,
    precision_score,
    recall_score,
)


mlflow.set_experiment("final_training")


def run_final_training(X_train, y_train, X_test, y_test):
    best_params = {
        "iterations": 304,
        "learning_rate": 0.06142931939577834,
        "depth": 8,
        "l2_leaf_reg": 3.1379883995374893,
        "subsample": 0.693900781099302,
        "eval_metric": "AUC",
        "loss_function": "Logloss",
        "auto_class_weights": "Balanced",
    }
    with mlflow.start_run():
        mlflow.log_params(best_params)
        model = catboost.CatBoostClassifier(**best_params)
        model.fit(
            X_train,
            y_train,
            verbose=0,
        )

        y_pred = model.predict(X_test)
        preds_proba = model.predict_proba(X_test)[:, 1]
        f1 = f1_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        auc = roc_auc_score(y_test, preds_proba)
        accuracy = accuracy_score(y_test, y_pred)

        mlflow.log_metric("f1_score", f1)
        mlflow.log_metric("roc_auc_score", auc)
        mlflow.log_metric("precision", precision)
        mlflow.log_metric("recall", recall)
        mlflow.log_metric("accuracy", accuracy)

        mlflow.catboost.log_model(model, "model")
    return model, f1, auc, precision, recall, accuracy
