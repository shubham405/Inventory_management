from django.shortcuts import render
import pickle

# Create your views here.
def index(request):
    return render(request,'Demo/index.html')
def tables(request):
    return render(request, 'Demo/tables.html')
def predict(request):
    if request.method == "POST":
        try:
            item_group = request.POST['itemGroup']
            shades = request.POST['shades']
            packSize = float(request.POST['packSize'])
            branchName = request.POST['branchName']
        
            IGEncoder = open('ItemGroup_encoder.pkl', 'rb')  
            itemEncoder  =pickle.load(IGEncoder)
            IGEncoder.close()
            item_group_tranformed = itemEncoder.transform([item_group])[0]
            shadesEncoder = open('Shade_encoder.pkl', 'rb')  
            sEncoder  =pickle.load(shadesEncoder)
            shadesEncoder.close()
            shades_transformed = sEncoder.transform([shades])[0]
            branchEncoder = open('NEW_Branch_Name_encoder.pkl', 'rb')  
            bEncoder  =pickle.load(branchEncoder)
            branchEncoder.close()
            branchName_transformed = bEncoder.transform([branchName])[0]
            print(item_group,branchName,shades)
            inventry_pkl = open('inventory_pred.pkl', 'rb')
            inventry_pred = pickle.load(inventry_pkl)
            inventry_pkl.close()
            scale = open('scaling.pkl', 'rb')
            scaling = pickle.load(scale)
            scale.close()
            temp=scaling.transform([[item_group_tranformed,shades_transformed,packSize,branchName_transformed]])
           # print(temp[0][0])
            result = inventry_pred.predict([[item_group_tranformed,shades_transformed,packSize,branchName_transformed]])
            #print("Predicted item quantity",result[0][0])
            result = f"Predicted item quantity for {item_group}, {shades}, {packSize}, {branchName} is {int(result[0][0])}"
        except Exception as e:
            result = f' Exception occur {e}' 
            #print(result)
        return render(request,'Demo/transactions.html',{'result': result})
            
    
        
    return render(request,'Demo/transactions.html')
def make_prediction(request):
    if request.method == "POST":
        pass 