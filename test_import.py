import sys
print("Python Path:")
for p in sys.path:
    print(f"  {p}")

print("\n" + "="*70)
print("Attempting import...")
print("="*70 + "\n")

try:
    from config.settings import Settings
    print("✅ SUCCESS!")
    print(f"Settings class: {Settings}")
    print(f"GOOGLE_API_KEY set: {bool(Settings.GOOGLE_API_KEY)}")
    print(f"GEMINI_MODEL: {Settings.GEMINI_MODEL}")
except ImportError as e:
    print(f"❌ FAILED: {e}")
    
    # Try alternate import
    print("\nTrying alternate import...")
    try:
        import config.settings as settings_module
        print(f"Module contents: {dir(settings_module)}")
    except Exception as e2:
        print(f"Also failed: {e2}")