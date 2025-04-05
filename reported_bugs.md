# 🐞 Bug Reports


# BUG #1

## 🧠 What’s the bug?

<!-- Brief description -->
Toggling column checkboxes (or clicking "Show All" / "Hide All") doesn’t actually update the table UI.

---

## ✅ Expected behavior

<!-- What should happen -->
All columns should actually be hidden including RA/DEC, or if they stay visible then their checkboxes should not also be deselected

---

## ❗Actual behavior

<!-- What is happening -->
RA/DEC stays visible but their checkboxes are deselected

---

## 🔁 Steps to Reproduce

1. Run the app
2. Execute a search to show results
3. Click the “Columns” button
4. Check hide all
5. All columns except RA and DEC are hidden, but every checkbox is unselected
6. Now you can select RA/DEC even tho they are visible and potentially causing state issues


---

## 🧩 Relevant code (snippets)
*INSERT HERE*

# BUG 2