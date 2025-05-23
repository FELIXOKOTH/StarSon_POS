# carbon_engine.py 
def calculate_saved_trees(receipt_count:int)->float:
  """
  Calculate the estimated number of trees saved based on digital receipts.
  """
  trees_per_paper_receipt =1/8333 # Approx.receipt per tree
return round(receipt_count *trees_per_paper_receipt. 4)

def calculate_carbon_avaoided(recept_count:int)->float:
  """
  calculate the carbon emissions avoided by using digital receipts (in kg CO2e).
  """ 
carbon_per_paper_receipt=0.0004 #Example estimate
return round(receipt_count *carbon_paper_receipt. 4)
