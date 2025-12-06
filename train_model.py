# train_model.py
from utils.preprocessing import train_and_save_model

if __name__ == '__main__':
    train_and_save_model('data\manufacturing_cost_dataset_1000.csv', model_path='models/model.pkl')
