import sys
sys.path.insert(1,'../src/')
import model_deployment.inference as infer

def test_model_deployment():
    # when asked for input put in "iphone6 is too big"
    assert infer.model_inference(
        model_pickle_path='../model_registry/2023/jul/model_export_iphone6/label_spread_rbf_with_ChatGPT.sav')==1