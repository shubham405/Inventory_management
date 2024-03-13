import pickle
import warnings
from sklearn.exceptions import InconsistentVersionWarning

# Suppress warnings related to inconsistent versions when unpickling
warnings.filterwarnings("ignore", category=InconsistentVersionWarning)
def makePrediction(df):
    try:
         IGEncoder = open("ItemGroup_encoder.pkl", "rb")
         itemEncoder = pickle.load(IGEncoder)
         IGEncoder.close()
        #  print("item group encoding")
         df.loc[:, 'Item Group']=itemEncoder.transform(df['Item Group'])
         shadesEncoder = open("Shade_encoder.pkl", "rb")
         sEncoder = pickle.load(shadesEncoder)
         shadesEncoder.close()
         df.loc[:, 'Shade'] = sEncoder.transform(df['Shade'])
         branchEncoder = open("branch_code.pkl", "rb")
         bEncoder = pickle.load(branchEncoder)
         branchEncoder.close()
         df.loc[:, 'Branch'] = bEncoder.transform(df['Branch'])
         inventry_pkl = open("inventory_pred.pkl", "rb")
         inventry_pred = pickle.load(inventry_pkl)
         inventry_pkl.close()
         result = inventry_pred.predict(df)
        #  print(result)
         return result
    except Exception as e:
         print(e)
         pass