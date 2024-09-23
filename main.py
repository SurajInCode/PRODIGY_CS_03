# password strength checker/evaluator by Suraj//
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import string
import secrets
import pyperclip
import math

# Entropy Calculation Function
def calculate_entropy(pwd):
    """Calculate the Shannon entropy of the password."""
    charset_size = 0
    if any(c in string.ascii_lowercase for c in pwd):
        charset_size += 26  # Lowercase letters
    if any(c in string.ascii_uppercase for c in pwd):
        charset_size += 26  # Uppercase letters
    if any(c in string.digits for c in pwd):
        charset_size += 10  # Digits
    if any(c in string.punctuation for c in pwd):
        charset_size += len(string.punctuation)  # Special characters

    if charset_size == 0:
        return 0

    entropy = len(pwd) * math.log2(charset_size)
    return entropy

def evaluate_password_strength(pwd):
    score = 0
    feedback = ''
    lower = upper = digits = spaces = specials = 0

    for ch in list(pwd):
        if ch in string.ascii_lowercase:
            lower += 1
        elif ch in string.ascii_uppercase:
            upper += 1
        elif ch in string.digits:
            digits += 1
        elif ch == ' ':
            spaces += 1
        else:
            specials += 1

    # Score based on character types
    if lower >= 1:
        score += 1
    if upper >= 1:
        score += 1
    if digits >= 1:
        score += 1
    if spaces >= 1:
        score += 1
    if specials >= 1:
        score += 1

    # Additional score based on length
    if len(pwd) >= 12:
        score += 1  # Extra point for longer passwords

    # Calculate entropy and provide feedback
    entropy = calculate_entropy(pwd)
    if entropy < 28:
        feedback = "🚨 Very Weak! Increase length and variety."
    elif entropy < 35:
        feedback = "⚠️ Weak. Try adding more character types."
    elif entropy < 50:
        feedback = "👍 Decent but could be stronger."
    elif entropy < 60:
        feedback = "✅ Good password!"
    else:
        feedback = "💪 Excellent password! Great job."

    return f'Your password has:\n{lower} lowercase letters\n{upper} uppercase letters\n{digits} digits\n{spaces} spaces\n{specials} special characters\nLength: {len(pwd)}\nEntropy: {entropy:.2f} bits\nRemarks: {feedback}', score

def verify_password():
    pwd = entry_pwd.get()
    result, score = evaluate_password_strength(pwd)
    text_output.config(state='normal')
    text_output.delete('1.0', 'end')
    text_output.insert('end', result)
    text_output.config(state='disabled')

    if score < 3:
        progress_meter["style"] = "Red.Horizontal.TProgressbar"
    elif score < 5:
        progress_meter["style"] = "Orange.Horizontal.TProgressbar"
    else:
        progress_meter["style"] = "Green.Horizontal.TProgressbar"

    animate_progress(progress_meter, score * 20, 0)

def create_password(length=12, use_specials=True):
    charset = string.ascii_letters + string.digits
    if use_specials:
        charset += string.punctuation
    pwd = ''.join(secrets.choice(charset) for _ in range(length))
    entry_pwd.delete(0, 'end')
    entry_pwd.insert('end', pwd)

def copy_to_clipboard():
    pwd = entry_pwd.get()
    if pwd:
        pyperclip.copy(pwd)
        messagebox.showinfo("Copied", "Password copied to clipboard!")

def clear_entry():
    entry_pwd.delete(0, 'end')

def toggle_password_visibility():
    if entry_pwd.cget('show') == '':
        entry_pwd.config(show='*')
        toggle_btn.config(text="👀 Show")
    else:
        entry_pwd.config(show='')
        toggle_btn.config(text="🙈 Hide")

def animate_progress(progressbar, target, current):
    step = (target - current) / 10  # Easing
    if abs(target - current) > 1:
        progressbar["value"] = current
        root.after(50, animate_progress, progressbar, target, current + step)
    else:
        progressbar["value"] = target

# Neon Button Hover Effect Functions
def on_enter(btn, color, glow_color):
    btn['background'] = color
    btn['foreground'] = glow_color
    btn['borderwidth'] = 2  # Increase border on hover

def on_leave(btn, color):
    btn['background'] = color
    btn['foreground'] = "black"
    btn['borderwidth'] = 2  # Reset border

# GUI Setup
root = tk.Tk()
root.title("Password Strength Evaluator")
root.geometry("650x450")

main_frame = tk.Frame(root, bg="#212121")  # Dark background for better neon effect
main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

label_pwd = tk.Label(main_frame, text="Enter the password:", bg="#212121", fg="white", font=("Helvetica", 14))
label_pwd.grid(row=0, column=0, padx=5, pady=5, sticky="we")

entry_pwd = tk.Entry(main_frame, show="*", font=("Helvetica", 12), bg="#333333", fg="white", insertbackground="white")
entry_pwd.grid(row=0, column=1, padx=5, pady=5, sticky="we", columnspan=2)

toggle_btn = tk.Button(main_frame, text="👁️ Show", command=toggle_password_visibility, bg="#8A2BE2", fg="black", font=("Helvetica", 12,"bold"), relief=tk.FLAT, borderwidth=2)
toggle_btn.grid(row=0, column=3, padx=5, pady=5, sticky="we")

btn_check = tk.Button(main_frame, text="Check", command=verify_password, bg="#39FF14", fg="black", font=("Helvetica", 12,"bold"), relief=tk.FLAT, borderwidth=2)
btn_check.grid(row=1, column=0, pady=10, padx=5, sticky="we")

btn_generate = tk.Button(main_frame, text="Generate Password", command=lambda: create_password(length=16), bg="#1E90FF", fg="white", font=("Helvetica", 12,"bold"), relief=tk.FLAT, borderwidth=2)
btn_generate.grid(row=1, column=1, pady=10, padx=5, sticky="we")

btn_copy = tk.Button(main_frame, text="Copy Password", command=copy_to_clipboard, bg="#FFFF33", fg="black", font=("Helvetica", 12,"bold"), relief=tk.FLAT, borderwidth=2)
btn_copy.grid(row=1, column=2, pady=10, padx=5, sticky="we")

btn_clear = tk.Button(main_frame, text="Clear", command=clear_entry, bg="#FF073A", fg="black", font=("Helvetica", 12,"bold"), relief=tk.FLAT, borderwidth=2)
btn_clear.grid(row=1, column=3, pady=10, padx=5, sticky="we")

text_output = tk.Text(main_frame, height=10, width=60, state='disabled', font=("Helvetica", 10), bg="#333333", fg="white", relief=tk.FLAT, borderwidth=2)
text_output.grid(row=2, column=0, columnspan=4, pady=10)

progress_meter = ttk.Progressbar(main_frame, orient=tk.HORIZONTAL, length=450, mode='determinate', value=0, style="Blue.Horizontal.TProgressbar")
progress_meter.grid(row=3, column=0, columnspan=4, pady=12)

entry_pwd.bind("<KeyRelease>", lambda event: verify_password())

# Add "By SurajInCode" label at the bottom-right corner
label_signature = tk.Label(root, text="By SurajInCode", font=("Helvetica", 12, "bold"), bg="#212121", fg="green")
label_signature.place(relx=1.0, rely=1.0, anchor="se", x=-20, y=-20)  # Adjusting position near the bottom-right corner


# Add hover effects with neon glow
buttons = [
    (btn_check, "#39FF14", "#7CFC00"),  # Neon green for "Check"
    (btn_generate, "#1E90FF", "#00BFFF"),  # Neon blue for "Generate"
    (btn_copy, "#FFFF33", "#FFD700"),  # Neon yellow for "Copy"
    (btn_clear, "#FF073A", "#FF6347"),  # Neon red for "Clear"
    (toggle_btn, "#8A2BE2", "#9370DB")  # Neon purple for "Show/Hide"
]

for btn, normal_color, glow_color in buttons:
    btn.bind("<Enter>", lambda e, b=btn, c=normal_color, g=glow_color: on_enter(b, c, g))
    btn.bind("<Leave>", lambda e, b=btn, c=normal_color: on_leave(b, c))

root.mainloop()
