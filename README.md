# Sort Lines (Numerically)

Sublime Text 2/3 package that adds a command for sorting lines numerically rather than alphabetically.

Installation
------------
This package is available through [Package Control](https://sublime.wbond.net/), it’s called “Sort Lines (Numerically)”.

Usage
-----
Just run “Sort Lines (Numerically)” from the Command Palette, or from the Edit menu, which has a keyboard shortcut as well.

Adding a reverse command
------------------------
This package does not have a reverse option when sorting, since there is already a `Reverse` command built into Sublime Text. If you want a shortcut for sorting numerically in reverse, you can make one yourself:

In your `User` package folder, create a file called `Sort Lines (Numerically) Reverse.sublime-macro`. Edit that file, paste in the following, and save:

```
[
	{
		"args": null,
		"command": "sort_numerically"
	},
	{
		"args": {
			"operation": "reverse"
		},
		"command": "permute_lines"
	}
]
```

There will now be a new menu item at `Tools` > `Macros` > `User` > `Sort Lines (Numerically) Reverse` that when selected will sort numerically and reverse the order. If you want this macro available in the command palette, create a file in your `User` folder called something like `SortLinesNumericallyReverse.sublime-commands` containing the following:

```
[
	{
		"caption": "Sort Lines (Numerically) Reverse",
		"command": "run_macro_file",
		"args": {
			"file": "Packages/User/Sort Lines (Numerically) Reverse.sublime-macro"
		}
	}
]
```

You will now have a command called `Sort Lines (Numerically) Reverse` in your command palette. If you want to bind this command to a keyboard shortcut, add something like the following to your default user keymap file (available at `Preferences` > `Key Bindings – User`:

```
{
	"keys": ["ctrl+shift+f5"],
	"command": "run_macro_file",
	"args": {
		"file": "Packages/User/Sort Lines (Numerically) Reverse.sublime-macro"
	}
}
```

Credits
-------
Thanks to Curtis Gibby ([@curtisgibby](https://github.com/curtisgibby)) for contributions.
