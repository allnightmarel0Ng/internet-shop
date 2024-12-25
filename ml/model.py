import pandas as pd
from surprise import Dataset, Reader, SVD
from surprise.model_selection import train_test_split
from surprise.accuracy import rmse, mae
import pickle

class RecommendationSystem:
    def __init__(self, data: pd.DataFrame):
        """
        Args:
            data (pd.DataFrame): Dataset containing the data.
        """
        self.data = data
        self.model = None
        self.trainset = None
        self.testset = None

    def load_data(self):
        """
        Prepares the data for training.
        """
        reader = Reader(rating_scale=(self.data['rating'].min(), self.data['rating'].max()))
        surprise_data = Dataset.load_from_df(
            self.data[['user_id', 'item_id', 'rating']], reader
        )
        self.trainset, self.testset = train_test_split(surprise_data, test_size=0.25, random_state=42)
        print("Data loaded and split into train and test sets.")

    def train_model(self):
        """
        Trains the model using SVD.
        """
        self.model = SVD(random_state=42)
        self.model.fit(self.trainset)
        print("Model trained using SVD.")

    def get_metrics(self):
        """
        Computes evaluation metrics for the model.
        """
        if not self.model or not self.testset:
            raise ValueError("Model or test set not found. Train the model and load data first.")

        predictions = self.model.test(self.testset)
        rmse_error = rmse(predictions, verbose=False)
        mae_error = mae(predictions, verbose=False)
        return {"RMSE": rmse_error, "MAE": mae_error}

    def evaluate_model(self):
        """
        Evaluates the trained model and prints metrics.
        """
        metrics = self.get_metrics()
        print(f"Evaluation Metrics:\nRMSE: {metrics['RMSE']}\nMAE: {metrics['MAE']}")
        return metrics

    def recommend_items(self, user_id, top_n=10):
        """
        Recommends top N items for a given user.

        Returns:
            list: List of recommended item IDs.
        """
        if not self.model:
            self.load_model("recommender_model.pkl")

        user_rated_items = self.data[self.data['user_id'] == user_id]['item_id'].tolist()

        if not user_rated_items:
            popular_items = (
                self.data.groupby('item_id')['rating']
                .count()
                .sort_values(ascending=False)
                .head(top_n)
                .index.tolist()
            )
            return popular_items

        all_items = self.data['item_id'].unique()
        items_to_predict = [item for item in all_items if item not in user_rated_items]

        predictions = [
            (item, self.model.predict(user_id, item).est)
            for item in items_to_predict
        ]

        recommendations = sorted(predictions, key=lambda x: x[1], reverse=True)[:top_n]
        return [item for item, _ in recommendations]

    def save_model(self, file_path):
        """
        Saves the trained model to a file.

        Args:
            file_path (str): Path to save the model.
        """
        if not self.model:
            raise ValueError("Model not trained. Train the model first.")
        with open(file_path, 'wb') as file:
            pickle.dump(self.model, file)
        print(f"Model saved to {file_path}.")

    def load_model(self, file_path):
        """
        Loads a model from a file.

        Args:
            file_path (str): Path to the saved model.
        """
        with open(file_path, 'rb') as file:
            self.model = pickle.load(file)
        print(f"Model loaded from {file_path}.")

