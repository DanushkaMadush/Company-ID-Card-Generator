import tkinter as tk
from tkinter import filedialog, messagebox
from tkcalendar import DateEntry
from PIL import Image, ImageDraw, ImageFont
import qrcode
import os

# Function to generate the ID card
def generate_id():
    try:
        # Load the front and back template
        front_template = Image.open("id_front_template.jpg")
        back_template = Image.open("id_back_template.jpg")
        font = ImageFont.truetype("arial.ttf", size=24)

        # Add details to the front
        draw_front = ImageDraw.Draw(front_template)
        draw_front.text((150, 50), f"Name: {entry_name.get()}", font=font, fill="white")
        draw_front.text((150, 100), f"Staff No: {entry_staff_no.get()}", font=font, fill="white")
        draw_front.text((150, 150), f"Designation: {entry_designation.get()}", font=font, fill="white")
        draw_front.text((150, 200), f"NIC: {entry_nic.get()}", font=font, fill="white")
        draw_front.text((150, 250), f"Date Joined: {entry_date_joined.get()}", font=font, fill="white")

        # Paste employee image if uploaded
        if employee_image_path:
            emp_img = Image.open(employee_image_path).resize((100, 100))
            front_template.paste(emp_img, (50, 50))

        # Add details to the back
        draw_back = ImageDraw.Draw(back_template)
        draw_back.text((150, 50), f"Date of Issue: {entry_date_of_issue.get()}", font=font, fill="white")

        # Paste holder and officer signature images
        if holder_signature_path:
            holder_signature = Image.open(holder_signature_path).resize((100, 50))
            back_template.paste(holder_signature, (150, 100))
        if officer_signature_path:
            officer_signature = Image.open(officer_signature_path).resize((100, 50))
            back_template.paste(officer_signature, (150, 200))

        # Generate and add QR code to the back
        qr_data = f"Name: {entry_name.get()}, Staff No: {entry_staff_no.get()}"
        qr = qrcode.make(qr_data).resize((100, 100))
        back_template.paste(qr, (50, 300))

        # Save the output
        output_dir = "output_ids"
        os.makedirs(output_dir, exist_ok=True)
        front_template.save(os.path.join(output_dir, f"{entry_staff_no.get()}_front.jpg"))
        back_template.save(os.path.join(output_dir, f"{entry_staff_no.get()}_back.jpg"))
        messagebox.showinfo("Success", "ID card generated successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Function to browse and select an image
def browse_image(label):
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if file_path:
        label.config(text="Image Selected", fg="light green")
        return file_path
    else:
        label.config(text="No Image Selected", fg="red")
        return None

# Function to clear all inputs
def clear_inputs():
    entry_name.delete(0, tk.END)
    entry_staff_no.delete(0, tk.END)
    entry_designation.delete(0, tk.END)
    entry_nic.delete(0, tk.END)
    entry_date_joined.set_date("")
    entry_date_of_issue.set_date("")
    global employee_image_path, holder_signature_path, officer_signature_path
    employee_image_path = holder_signature_path = officer_signature_path = None
    lbl_image_status.config(text="No Image Selected", fg="red")
    lbl_holder_signature_status.config(text="No Image Selected", fg="red")
    lbl_officer_signature_status.config(text="No Image Selected", fg="red")

# Initialize Tkinter app
app = tk.Tk()
app.title("Employee ID Generator")
app.configure(bg="#2C2C2C")

# Labels and Entry Widgets for Front ID Details
tk.Label(app, text="Employee Name:", bg="#2C2C2C", fg="white").grid(row=0, column=0, sticky="w", padx=10, pady=5)
entry_name = tk.Entry(app, width=30, bg="#4D4D4D", fg="white", insertbackground="white")
entry_name.grid(row=0, column=1, padx=10, pady=5)

tk.Label(app, text="Staff No:", bg="#2C2C2C", fg="white").grid(row=1, column=0, sticky="w", padx=10, pady=5)
entry_staff_no = tk.Entry(app, width=30, bg="#4D4D4D", fg="white", insertbackground="white")
entry_staff_no.grid(row=1, column=1, padx=10, pady=5)

tk.Label(app, text="Designation:", bg="#2C2C2C", fg="white").grid(row=2, column=0, sticky="w", padx=10, pady=5)
entry_designation = tk.Entry(app, width=30, bg="#4D4D4D", fg="white", insertbackground="white")
entry_designation.grid(row=2, column=1, padx=10, pady=5)

tk.Label(app, text="NIC:", bg="#2C2C2C", fg="white").grid(row=3, column=0, sticky="w", padx=10, pady=5)
entry_nic = tk.Entry(app, width=30, bg="#4D4D4D", fg="white", insertbackground="white")
entry_nic.grid(row=3, column=1, padx=10, pady=5)

tk.Label(app, text="Date Joined:", bg="#2C2C2C", fg="white").grid(row=4, column=0, sticky="w", padx=10, pady=5)
entry_date_joined = DateEntry(app, width=27, background="#4D4D4D", foreground="white")
entry_date_joined.grid(row=4, column=1, padx=10, pady=5)

# Employee Image Upload
tk.Label(app, text="Employee Image:", bg="#2C2C2C", fg="white").grid(row=5, column=0, sticky="w", padx=10, pady=5)
lbl_image_status = tk.Label(app, text="No Image Selected", bg="#2C2C2C", fg="red")
lbl_image_status.grid(row=6, column=1, sticky="w", padx=10, pady=5)
employee_image_path = None
tk.Button(app, text="Browse", command=lambda: setattr(globals(), 'employee_image_path', browse_image(lbl_image_status)), bg="#4D4D4D", fg="white").grid(row=5, column=1, sticky="w", padx=10)

# Labels and Entry Widgets for Back ID Details
tk.Label(app, text="Date of Issue:", bg="#2C2C2C", fg="white").grid(row=7, column=0, sticky="w", padx=10, pady=5)
entry_date_of_issue = DateEntry(app, width=27, background="#4D4D4D", foreground="white")
entry_date_of_issue.grid(row=7, column=1, padx=10, pady=5)

tk.Label(app, text="Holder Signature:", bg="#2C2C2C", fg="white").grid(row=8, column=0, sticky="w", padx=10, pady=5)
lbl_holder_signature_status = tk.Label(app, text="No Image Selected", bg="#2C2C2C", fg="red")
lbl_holder_signature_status.grid(row=9, column=1, sticky="w", padx=10, pady=5)
holder_signature_path = None
tk.Button(app, text="Browse", command=lambda: setattr(globals(), 'holder_signature_path', browse_image(lbl_holder_signature_status)), bg="#4D4D4D", fg="white").grid(row=8, column=1, sticky="w", padx=10)

tk.Label(app, text="Officer Signature:", bg="#2C2C2C", fg="white").grid(row=10, column=0, sticky="w", padx=10, pady=5)
lbl_officer_signature_status = tk.Label(app, text="No Image Selected", bg="#2C2C2C", fg="red")
lbl_officer_signature_status.grid(row=11, column=1, sticky="w", padx=10, pady=5)
officer_signature_path = None
tk.Button(app, text="Browse", command=lambda: setattr(globals(), 'officer_signature_path', browse_image(lbl_officer_signature_status)), bg="#4D4D4D", fg="white").grid(row=10, column=1, sticky="w", padx=10)

# Buttons
tk.Button(app, text="Generate ID Card", command=generate_id, bg="#008000", fg="white", width=20).grid(row=12, column=0, padx=(10, 5), pady=20, sticky="e")
tk.Button(app, text="Clear", command=clear_inputs, bg="#8B0000", fg="white", width=20).grid(row=12, column=1, padx=(5, 10), pady=20, sticky="w")

# Run the Tkinter app
app.mainloop()
