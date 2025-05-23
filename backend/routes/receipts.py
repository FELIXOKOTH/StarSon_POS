from services.carbon_engine import calculate_saved_receipts,
calculate_carbon_avoided

@app.get("/eco-report")
def eco-report(total_receipts:int):
  tress=calcculate_saved_trees(total_receipts)
  carbon=calculate_carbon_avoide(total_rteceipts)
  return{"trees_saved":trees,"carbon_avoided_kg":carbo}
