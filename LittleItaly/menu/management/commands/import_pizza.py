from menu.utils import fetch_recipes

from django.core.management.base import BaseCommand

from menu.models import Recipe

class Command(BaseCommand):
    help = "Import recipes from the Edamam Recipe API."
    def handle(self, *args, **kwargs):
        try:
            data = fetch_recipes(query="pizza")
            recipes = data.get("hits", [])
            for recipe_data in recipes:
                recipe = recipe_data.get("recipe", {})
                # Validate the recipe.
                name = recipe.get("label", "Unknown Recipe")
                image = recipe.get("image", "")
                health_labels = ", ".join(recipe.get("healthLabels", []))
                cuisine_type = ", ".join(recipe.get("cuisineType", []))
                calories = recipe.get("calories", 0)
                total_nutrients = recipe.get("totalNutrients", {})
                ingredients = ", ".join(recipe.get("ingredientLines", []))
                # Create or update the recipe.
                Recipe.objects.update_or_create(
                    name=name,
                    defaults={
                        "image": image,
                        "healthLabels": health_labels,
                        "cuisineType": cuisine_type,
                        "calories": calories,
                        "totalNutrients": total_nutrients,
                        "ingredients": ingredients,
                    },
                )
            self.stdout.write(self.style.SUCCESS(f"Imported {len(recipes)} recipes."))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"An error occurred: {e}"))
