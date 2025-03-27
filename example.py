from engine import SamplesLibGenerate

generate_samples = SamplesLibGenerate()

for _ in range(8):
    notes = generate_samples.get_notes()
    print(notes)