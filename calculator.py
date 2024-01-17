import tkinter as tk

# Define color constants for dark mode
BACKGROUND_COLOR = "#121212"
BUTTON_COLOR = "#2E2E2E"
DISPLAY_COLOR = "#323232"
LABEL_COLOR = "#FFFFFF"
TEXT_COLOR = "#FFFFFF"
ERROR_COLOR = "#FF4747"

# Define font styles
LARGE_FONT_STYLE = ("Arial", 40, "bold")
SMALL_FONT_STYLE = ("Arial", 16)
DIGITS_FONT_STYLE = ("Arial", 24, "bold")
DEFAULT_FONT_STYLE = ("Arial", 20)

class Calculator:
    def __init__(self):
        # Initialize the calculator window
        self.window = tk.Tk()
        self.window.geometry("375x467")
        self.window.resizable(0, 0)
        self.window.title("Calculator")
        self.window.configure(bg=BACKGROUND_COLOR)

        # Initialize expression variables
        self.total_expression = ""
        self.current_expression = ""

        # Create display frame and labels
        self.display_frame = self.create_display_frame()
        self.total_label, self.label = self.create_display_labels()

        # Define digit and operation mappings
        self.digits = {
            7: (1, 1), 8: (1, 2), 9: (1, 3),
            4: (2, 1), 5: (2, 2), 6: (2, 3),
            1: (3, 1), 2: (3, 2), 3: (3, 3),
            0: (4, 2), '.': (4, 1)
        }
        self.operations = {"/": "÷", "*": "×", "-": "-", "+": "+"}

        # Create buttons frame and configure row/column weights
        self.buttons_frame = self.create_buttons_frame()
        self.buttons_frame.rowconfigure(0, weight=1)
        for x in range(1, 5):
            self.buttons_frame.rowconfigure(x, weight=1)
            self.buttons_frame.columnconfigure(x, weight=1)

        # Create digit, operator, and special buttons
        self.create_digit_buttons()
        self.create_operator_buttons()
        self.create_special_buttons()

        # Bind keys for keyboard input
        self.bind_keys()

    def bind_keys(self):
        # Bind Enter key for evaluation
        self.window.bind("<Return>", lambda event: self.evaluate())
        
        # Bind digit keys
        for key in self.digits:
            self.window.bind(str(key), lambda event, digit=key: self.add_to_expression(digit))

        # Bind operation keys
        for key in self.operations:
            self.window.bind(key, lambda event, operator=key: self.append_operator(operator))

    def create_special_buttons(self):
        # Create clear, equals, square, and square root buttons
        self.create_clear_button()
        self.create_equals_button()
        self.create_square_button()
        self.create_sqrt_button()

    def create_display_labels(self):
        # Create total and current expression labels
        total_label = tk.Label(self.display_frame, text=self.total_expression, anchor=tk.E, bg=DISPLAY_COLOR,
                               fg=LABEL_COLOR, padx=24, font=SMALL_FONT_STYLE)
        total_label.pack(expand=True, fill='both')

        label = tk.Label(self.display_frame, text=self.current_expression, anchor=tk.E, bg=DISPLAY_COLOR,
                         fg=TEXT_COLOR, padx=24, font=LARGE_FONT_STYLE)
        label.pack(expand=True, fill='both')

        return total_label, label

    def create_display_frame(self):
        # Create display frame
        frame = tk.Frame(self.window, height=221, bg=BACKGROUND_COLOR)
        frame.pack(expand=True, fill="both")
        return frame

    def add_to_expression(self, value):
        # Add digit or decimal point to the current expression
        self.current_expression += str(value)
        self.update_label()

    def create_digit_buttons(self):
        # Create digit buttons
        for digit, grid_value in self.digits.items():
            button = tk.Button(self.buttons_frame, text=str(digit), bg=BUTTON_COLOR, fg=LABEL_COLOR, font=DIGITS_FONT_STYLE,
                               borderwidth=0, command=lambda x=digit: self.add_to_expression(x))
            button.grid(row=grid_value[0], column=grid_value[1], sticky=tk.NSEW)

    def append_operator(self, operator):
        # Append operator to the current expression and update total expression
        self.current_expression += operator
        self.total_expression += self.current_expression
        self.current_expression = ""
        self.update_total_label()
        self.update_label()

    def create_operator_buttons(self):
        # Create operator buttons
        i = 0
        for operator, symbol in self.operations.items():
            button = tk.Button(self.buttons_frame, text=symbol, bg=BUTTON_COLOR, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                               borderwidth=0, command=lambda x=operator: self.append_operator(x))
            button.grid(row=i, column=4, sticky=tk.NSEW)
            i += 1

    def clear(self):
        # Clear both total and current expressions
        self.current_expression = ""
        self.total_expression = ""
        self.update_label()
        self.update_total_label()

    def create_clear_button(self):
        # Create clear button
        button = tk.Button(self.buttons_frame, text="C", bg=BUTTON_COLOR, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=0, command=self.clear)
        button.grid(row=0, column=1, sticky=tk.NSEW)

    def square(self):
        # Square the current expression
        self.current_expression = str(eval(f"{self.current_expression}**2"))
        self.update_label()

    def create_square_button(self):
        # Create square button
        button = tk.Button(self.buttons_frame, text="x²", bg=BUTTON_COLOR, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=0, command=self.square)
        button.grid(row=0, column=2, sticky=tk.NSEW)

    def sqrt(self):
        # Calculate the square root of the current expression
        self.current_expression = str(eval(f"{self.current_expression}**0.5"))
        self.update_label()

    def create_sqrt_button(self):
        # Create square root button
        button = tk.Button(self.buttons_frame, text="√", bg=BUTTON_COLOR, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=0, command=self.sqrt)
        button.grid(row=0, column=3, sticky=tk.NSEW)

    def evaluate(self):
        # Evaluate the total expression
        self.total_expression += self.current_expression
        self.update_total_label()
        try:
            self.current_expression = str(eval(self.total_expression))
            self.total_expression = ""
        except Exception as e:
            self.current_expression = "Error"
        finally:
            self.update_label()

    def create_equals_button(self):
        # Create equals button
        button = tk.Button(self.buttons_frame, text="=", bg=BUTTON_COLOR, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=0, command=self.evaluate)
        button.grid(row=4, column=3, columnspan=2, sticky=tk.NSEW)

    def create_buttons_frame(self):
        # Create buttons frame
        frame = tk.Frame(self.window, bg=BACKGROUND_COLOR)
        frame.pack(expand=True, fill="both")
        return frame

    def update_total_label(self):
        # Update the total expression label with formatted operators
        expression = self.total_expression
        for operator, symbol in self.operations.items():
            expression = expression.replace(operator, f' {symbol} ')
        self.total_label.config(text=expression)

    def update_label(self):
        # Update the current expression label
        self.label.config(text=self.current_expression[:11])

    def run(self):
        # Run the calculator application
        self.window.mainloop()


if __name__ == "__main__":
    calc = Calculator()
    calc.run()
