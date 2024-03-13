from django.shortcuts import render
import pickle
from django.http import HttpResponse
import pandas as pd
from .helper import makePrediction
import io


# Create your views here.
def index(request):
    return render(request, "Demo/index.html")


def tables(request):
    if request.method == "POST" and "file" in request.FILES:
        try:
            uploaded_file = request.FILES["file"]
            df = pd.read_excel(uploaded_file)
            # print(df.columns)

            df = df.dropna()
            # df["Branch"] = df["Branch"].str.split().apply(lambda x: x[2])
            # df["Branch"] = df["Branch"].apply(
            #     lambda x: "PAINTS-(HO)" if x == "PAINTS" else x
            # )
            # print(df)
            df = df[["Item Group", "Shade", "Pack Size", "Branch"]]
            file_path = 'test.xlsx'

# Save the DataFrame to an Excel file
            df.to_excel(file_path, index=False)
            temp = df.copy()
            results = makePrediction(temp)
            # print(results)
            # df = df.reset_index(drop=True)
            if len(results) == len(df):
                # Assign values to the new column
                df["Predicted Quantity"] = [abs(int(item[0])) for item in results]
            else:
                print(
                    "Length of data does not match the number of rows in the DataFrame."
                )
            print(df)
            final_result = df
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
                final_result.to_excel(writer, sheet_name="final_result", index=True)
            output.seek(0)
            # grouped_df = df.groupby("Branch")
            # # res = {}
            # for name, group in grouped_df:
            #     # res[name] = []
            #     #print(name)
            #     if name  == 'PAINTS-(DEHRADUN)':
            #         group = group[['Item Group','Shade','Pack Size','Branch']]
            #         temp = group.copy()
            #         results = makePrediction(temp)
            #         for res in results[0]:
            #             group

            #         # print(res)
            #         print(group)
            #         if res is not None and name  == 'OZELL COONER PAINTS-(DEHRADUN)':
            #             print(res)
            response = HttpResponse(
                output,
                content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
            response["Content-Disposition"] = "attachment; filename=final_result.xlsx"
            return response
        except Exception as e:
            error_msg = "Some error occured"
            return render(request, "Demo/tables.html", {"error_message": error_msg})
    return render(request, "Demo/tables.html")


def predict(request):
    if request.method == "POST":
        try:
            item_group = request.POST["itemGroup"]
            shades = request.POST["shades"]
            packSize = float(request.POST["packSize"])
            branchName = request.POST["branchName"]

            IGEncoder = open("ItemGroup_encoder.pkl", "rb")
            itemEncoder = pickle.load(IGEncoder)
            IGEncoder.close()
            item_group_tranformed = itemEncoder.transform([item_group])[0]
            shadesEncoder = open("Shade_encoder.pkl", "rb")
            sEncoder = pickle.load(shadesEncoder)
            shadesEncoder.close()
            shades_transformed = sEncoder.transform([shades])[0]
            branchEncoder = open("branch_code.pkl", "rb")
            bEncoder = pickle.load(branchEncoder)
            branchEncoder.close()
            branchName_transformed = bEncoder.transform([branchName])[0]
            print(item_group, branchName, shades)
            inventry_pkl = open("inventory_pred.pkl", "rb")
            inventry_pred = pickle.load(inventry_pkl)
            inventry_pkl.close()
            # scale = open('scaling.pkl', 'rb')
            # scaling = pickle.load(scale)
            # scale.close()
            # temp=scaling.transform([[item_group_tranformed,shades_transformed,packSize,branchName_transformed]])
            # print(temp[0][0])
            result = inventry_pred.predict(
                [
                    [
                        item_group_tranformed,
                        shades_transformed,
                        packSize,
                        branchName_transformed,
                    ]
                ]
            )
            # print("Predicted item quantity",result[0][0])
            result = f"Predicted item quantity for {item_group}, {shades}, {packSize}, {branchName} is {int(result[0][0])}"
        except Exception as e:
            result = f" Exception occur {e}"
            # print(result)
        return render(request, "Demo/transactions.html", {"result": result})

    return render(request, "Demo/transactions.html")


def make_prediction(request):
    if request.method == "POST":
        pass
