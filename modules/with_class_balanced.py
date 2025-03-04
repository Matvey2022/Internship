import mlflow
import mlflow.catboost
import optuna
import catboost
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    roc_auc_score,
    precision_score,
    recall_score,
)


mlflow.set_experiment("With_class_balanced")


def run_optimization(X_train, y_train, X_valid, y_valid):
    def objective(trial: optuna.Trial):
        params = {
            "iterations": trial.suggest_int("iterations", 100, 1000),
            "learning_rate": trial.suggest_float("learning_rate", 0.01, 0.3),
            "depth": trial.suggest_int("depth", 4, 10),
            "l2_leaf_reg": trial.suggest_float("l2_leaf_reg", 1, 10),
            "subsample": trial.suggest_float("subsample", 0.5, 1.0),
            "eval_metric": "AUC",
            "loss_function": "Logloss",
            "auto_class_weights": "Balanced",
        }

        with mlflow.start_run():
            mlflow.log_params(params)
            model = catboost.CatBoostClassifier(**params)  # moved from fit method
            model.fit(
                X_train,
                y_train,
                eval_set=(X_valid, y_valid),
                early_stopping_rounds=50,
                verbose=0,
            )
            y_pred = model.predict(X_valid)
            # Predict probabilities for the positive class (class 1).
            # The predict_proba method returns a 2D array where each row represents a sample
            # and each column represents a class. We take the second column (index 1)
            # which corresponds to the probability of the positive class.
            preds_proba = model.predict_proba(X_valid)[:, 1]

            f1 = f1_score(y_valid, y_pred)
            precision = precision_score(y_valid, y_pred)
            recall = recall_score(y_valid, y_pred)
            auc = roc_auc_score(y_valid, preds_proba)
            accuracy = accuracy_score(y_valid, y_pred)

            mlflow.log_metric("f1_score", f1)
            mlflow.log_metric("roc_auc_score", auc)
            mlflow.log_metric("precision", precision)
            mlflow.log_metric("recall", recall)
            mlflow.log_metric("accuracy", accuracy)

            mlflow.catboost.log_model(model, "model")
        return auc

    study = optuna.create_study(direction="maximize")
    study.optimize(objective, n_trials=100)
    return study
