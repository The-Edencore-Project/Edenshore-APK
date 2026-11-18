from pythonforandroid.recipe import Recipe
from pythonforandroid.recipes.libthorvg import LibThorvgRecipe as OriginalLibThorvgRecipe
import os

class LibThorvgRecipe(OriginalLibthorvgRecipe):
    patches = ['fix_clang_lib_dir.patch']

recipe = LibThorvgRecipe()