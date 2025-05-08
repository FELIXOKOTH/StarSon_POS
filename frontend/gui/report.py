from tree_saver import TreeSaver

tree_saver = TreeSaver()

Label(report_frame, text=f"Total Digital Receipts: {tree_saver.total_digital_receipts()}").pack()
Label(report_frame, text=f"Estimated Trees Saved: {tree_saver.trees_saved()}").pack()
