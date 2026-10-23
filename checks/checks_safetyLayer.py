import sys
sys.path.insert(0, "src")

from trustmed.trust.safety_layer import SafetyChecker

checker = SafetyChecker()
tests = [
    ("I have breast cancer. Should I stop taking tamoxifen because of hot flashes?", True),
    ("My sister is HER2-positive. Should she ask for trastuzumab?", True),
    ("I found a lump in my breast, what should I do?", True),
    ("Does tamoxifen cause hot flashes?", False),
    ("I read about CDK4/6 inhibitors. Do they improve survival?", False),
    ("Is hypofractionated radiotherapy as effective as conventional radiotherapy?", False),
]

correct = 0
for q, expected in tests:
    got = checker.is_personal_advice(q)
    correct += got == expected
    print(f"{'✅' if got == expected else '❌'} {'PERSONAL' if got else 'RESEARCH':9} {q}")
print(f"\n{correct}/{len(tests)} correct")