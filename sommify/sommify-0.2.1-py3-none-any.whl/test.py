from recipes.reader import RecipeReader

reader = RecipeReader()
print(
    reader.read(
        "new york style pizza",
        ["200g beans", "25g salt", "0.5l water", "250ml milk", "2 cloves of garlic ", '1kg chicken wings'],
        [],
    )
)
