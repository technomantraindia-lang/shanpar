# -*- coding: utf-8 -*-
"""Shanpar site content, transcribed from the company brochure (pages 3-5)
and the Mujpur plant presentation (Shanpar_Presentation_Mujpur 21-08-25.ppt).

Product line format:  "Name | qualifier | new"
  qualifier  = the italic hydrate/form note in the brochure (may be empty)
  new        = "new" when the brochure marks the product with a NEW flag
"""

# ---------------------------------------------------------------- products
# Brochure page 4: BP / IP / USP / NF / FCC grade
# (API, Nutraceuticals, Mineral fortifiers, Mineral premix)
PHARMA = """
Calcium aspartate | anhydrous |
Calcium citrate | tetrahydrate/anhydrous |
Calcium citrate malate/maleate | |
Calcium copper edetate | | new
Calcium ferrous citrate | |
Calcium fumarate | |
Calcium glubionate | |
Calcium gluconate | anhy./mono. |
Calcium glycinate | |
Calcium lactobionate | |
Calcium levulinate | |
Calcium malate | |
Calcium orotate | dihydrate |
Calcium pidolate | |
Calcium pyruvate | |
Calcium saccharate | |
Calcium sodium edetate | |
Calcium succinate | |
Calcium sulfate | |
Calcium undecylenate | |
Copper citrate | |
Copper gluconate | |
Copper glycinate | |
Copper disodium edetate | |
Copper lysinate | |
Chromium 0.2% in maltodextrin premix | | new
Choline dihydrogen citrate | |
Choline bitartrate | |
Chlorobutanol | hemihydrate/anhydrous |
Ferric ammonium citrate | |
Ferric orthophosphate | |
Ferric pyrophosphate | soluble/insoluble |
Ferric sodium edetate | |
Ferrous citrate | |
Ferrous fumarate | |
Ferrous gluconate | |
Ferrous lactate | |
Ferrous succinate | |
Magnesium aspartate | |
Magnesium citrate | anhy./hyd. |
Magnesium citrate soluble | |
Magnesium fumarate | |
Magnesium gluconate | |
Magnesium glycinate | |
Magnesium lactate | |
Magnesium maleate | |
Magnesium orotate | dihydrate |
Magnesium phosphate | di/tri basic |
Manganese citrate | |
Manganese gluconate | anhy./dried |
Manganese orotate | |
Potassium aspartate | |
Potassium glucarate | |
Potassium gluconate | |
Potassium magnesium citrate | |
Potassium malate | | new
Potassium pyrophosphate | |
Selenium dioxide | |
Selenium sulfide | | new
Sodium ferrous citrate | | new
Sodium ferro edetate | |
Sodium fumarate | mono./di. |
Sodium gluconate | |
Sodium molybdate 1% in maltodextrin premix | | new
Sodium selenate/selenite | |
Sodium selenite 1% in maltodextrin premix | | new
Sodium selenite 1% in sodium citrate premix | | new
Sodium stibogluconate | |
Vanadyl sulfate | | new
Vanadium 1% triturate in DCP premix | | new
Zinc aspartate | |
Zinc citrate | di/trihydrate |
Zinc citrate soluble | |
Zinc fumarate | |
Zinc gluconate | |
Zinc glycinate | |
Zinc lactate | |
Zinc lysinate | |
Zinc maleate | |
Zinc orotate | |
Zinc picolinate | |
Zinc succinate | |
Chromium picolinate | |
Fumaric acid | |
Iodoform | |
"""

# Brochure page 5: Pure / ACS grade (Speciality chemicals)
ACS = """
Ammonium adipate | |
Ammonium benzoate | |
Ammonium citrate | dibasic/tribasic |
Ammonium lactate solution | |
Ammonium propionate | |
Betaine dihydrogen citrate | | new
Bismuth citrate | |
Bismuth subcarbonate | |
Bismuth subsalicylate | |
Boron citrate/gluconate | |
Chromium amino acid chelate | | new
Chlorobutanol | |
Cadmium chloride | |
Cadmium sulfate | |
Calcium acid pyrophosphate | | new
Calcium alpha ketoglutarate | | new
Calcium benzoate | |
Calcium copper edetate | | new
Calcium lysinate | |
Calcium peroxide | |
Calcium propionate | |
Calcium saccharate | |
Copper lysinate hydrochloride | |
Copper pyrophosphate | |
Cobalt gluconate | |
Ferric orthophosphate | |
Ferric pyrophosphate | |
Ferrous bisglycinate | | new
Ferrous glutamate | |
Ferrous lactate | |
Lithium orotate | |
L-Lysine hydrochloride | |
Magnesium lactate | |
Magnesium peroxide | |
Manganese lactate | | new
Nickel bromide | |
Nickel citrate | |
Nickel formate | |
Potassium benzoate | |
Potassium glucarate | | new
Potassium gluconate | |
Potassium pyrophosphate | |
Potassium magnesium aspartate | |
Potassium malate | | new
Potassium sorbate | |
Selenium sulfide | | new
Sodium ferrous citrate | |
Sodium ferric pyrophosphate | | new
Sodium gluconate | |
Sodium pyrophosphate | |
Sodium selenate/selenite | |
Strontium acetate | |
Strontium chloride | |
Strontium citrate | |
Strontium carbonate | |
Strontium hydroxide | |
Strontium lactate | | new
Vanadium citrate | | new
Vanadyl sulfate | | new
Zinc benzoate | |
Zinc bromide | |
Zinc peroxide | |
Barium peroxide | |
Gluconic acid | |
Iodoform | |
Thiourea | |
Taurine | |
"""

# ---------------------------------------------------------------- categories
# (slug, title, keywords matched in order, short intro)
CATEGORIES = [
    ("mineral-premixes", "Mineral Premixes", ["premix", "triturate"],
     "Trace minerals diluted on a carrier such as maltodextrin, sodium citrate or DCP. Premixes make microgram-level minerals like selenium, chromium and molybdenum easy to dose evenly in tablets, capsules and fortified foods."),
    ("citrates", "Citrates", ["citrate"],
     "Salts of citric acid. Mineral citrates dissolve well and are widely used in supplements, effervescent products and fortified foods and beverages."),
    ("gluconates", "Gluconates", ["gluconate", "glubionate", "gluconic"],
     "Salts of gluconic acid, the product line Shanpar was founded on in 1982. Gluconates are soluble and mild in taste, which makes them common in oral solutions, syrups, tablets and food fortification."),
    ("aspartates", "Aspartates", ["aspartate"],
     "Mineral salts of aspartic acid, an amino acid. Aspartates are used mainly in nutraceutical and pharmaceutical mineral formulations."),
    ("edetates", "Edetates", ["edetate"],
     "EDTA salts and metal-EDTA complexes. Edetates are used as chelating agents and as stable, well-absorbed mineral sources such as ferric sodium edetate for iron fortification."),
    ("glycinates-chelates", "Glycinates & Chelates", ["glycinate", "lysinate", "glutamate", "amino acid chelate", "picolinate"],
     "Minerals bound to amino acids or picolinic acid. Chelated minerals are popular in premium supplements for their stability and tolerance."),
    ("lactates", "Lactates", ["lactate"],
     "Salts of lactic acid. Mineral lactates are soluble and neutral in taste, suited to food fortification, beverages and pharmaceutical use."),
    ("fumarates", "Fumarates", ["fumarate", "fumaric"],
     "Salts of fumaric acid. Ferrous fumarate is one of the most widely used iron sources in supplements and fortified foods."),
    ("malates-maleates", "Malates & Maleates", ["malate", "maleate"],
     "Salts of malic and maleic acid, used as mineral sources in nutraceutical and food formulations."),
    ("orotates", "Orotates", ["orotate"],
     "Mineral salts of orotic acid, used in nutraceutical mineral formulations."),
    ("peroxides", "Peroxides", ["peroxide"],
     "Metal peroxides that release oxygen. They are used in speciality, dough-conditioning, cosmetic and environmental applications."),
    ("phosphates-pyrophosphates", "Phosphates & Pyrophosphates", ["phosphate"],
     "Ortho- and pyrophosphate salts. Ferric pyrophosphate and ferric orthophosphate are used where a colour-stable, low-reactivity iron source is needed."),
    ("succinates", "Succinates", ["succinate"],
     "Salts of succinic acid, used as mineral sources in pharmaceutical and nutraceutical products."),
    ("sulfates", "Sulfates", ["sulfate"],
     "Mineral sulfates for pharmaceutical, nutraceutical and speciality use."),
    ("benzoates-propionates", "Benzoates, Propionates & Sorbates", ["benzoate", "propionate", "sorbate"],
     "Salts of benzoic, propionic and sorbic acid, used mainly as preservatives in food, feed, cosmetic and pharmaceutical products."),
    ("other-compounds", "Other Speciality Compounds", [],
     "Benzoates, propionates, halides, bismuth compounds and other speciality chemicals, supplied mainly in Pure and ACS grades."),
]

# ---------------------------------------------------------------- elements
ELEMENT_WORDS = [
    ("Ca", ["calcium"]), ("Cu", ["copper"]), ("Cr", ["chromium"]),
    ("Fe", ["ferric", "ferrous", "ferro "]), ("Mg", ["magnesium"]),
    ("Mn", ["manganese"]), ("K", ["potassium"]), ("Se", ["selenium", "selenite", "selenate"]),
    ("Na", ["sodium"]), ("V", ["vanadyl", "vanadium"]), ("Zn", ["zinc"]),
    ("Bi", ["bismuth"]), ("B", ["boron"]), ("Cd", ["cadmium"]), ("Co", ["cobalt"]),
    ("Li", ["lithium"]), ("Ni", ["nickel"]), ("Sr", ["strontium"]), ("Ba", ["barium"]),
    ("Mo", ["molybdate"]), ("Sb", ["stibogluconate"]),
]
ELEMENT_NAMES = {
    "Ca": "Calcium", "Cu": "Copper", "Cr": "Chromium", "Fe": "Iron", "Mg": "Magnesium",
    "Mn": "Manganese", "K": "Potassium", "Se": "Selenium", "Na": "Sodium", "V": "Vanadium",
    "Zn": "Zinc", "Bi": "Bismuth", "B": "Boron", "Cd": "Cadmium", "Co": "Cobalt",
    "Li": "Lithium", "Ni": "Nickel", "Sr": "Strontium", "Ba": "Barium", "Mo": "Molybdenum",
    "Sb": "Antimony",
}

# ---------------------------------------------------------------- company (PPT)
PEOPLE = [
    ("Mr. B. N. Patel", "Managing Director", "M.Sc., Organic Chemistry", 50, "years as a technocrat and industrialist"),
    ("Mr. M. S. Yadav", "Technical Director", "M.Sc., Organic Chemistry", 30, "years in bulk drugs, nutraceuticals and fine chemicals"),
    ("Mr. Manish Joshi", "QC Manager", "M.Sc., Chemistry", 28, "years in quality control"),
    ("Ms. Meeta Panchal", "QA QC Manager", "M.Sc., Organic Chemistry", 27, "years in quality assurance and control"),
    ("Mr. Shailesh Shah", "Production Head", "", 30, "years in manufacturing and packing"),
    ("Mr. Chandrakant Solanki", "Engineering & Safety In-charge", "", 5, "years in engineering and industrial safety"),
]

STAFF = [  # department, management/staff, workmen
    ("Manufacturing & packing", 6, 68),
    ("Quality unit (QA-QC)", 18, 3),
    ("Engineering", 1, 7),
    ("Stores", 2, 2),
    ("Accounts & logistics", 5, 0),
    ("Sales & marketing", 3, 0),
    ("Purchase", 1, 0),
]

VISION = [
    "Maintain a manufacturing facility that meets GMP and FSSC standards for quality.",
    "Have a team of competent people who constantly maintain manufacturing, quality and ethical standards.",
    "Strive relentlessly to update and upgrade our systems, technology and knowledge.",
    "Keep improving systems and people for productivity and quality.",
    "Serve leading pharmaceutical and food companies and grow as partners of multinationals.",
]

POLICIES = ["Code of Conduct", "Corporate Social Responsibility", "Ethical Trade Policy",
            "Discrimination Policy", "Environment Policy", "Child Labour Policy",
            "Forced Labour Policy", "Personnel Health & Hygiene Policy", "Health & Safety Policy",
            "Allergen Policy", "Jewellery Policy", "Glass Policy"]

CUSTOMERS = ["Pfizer", "Abbott", "Nestlé", "GSK", "DSM", "Boehringer Ingelheim", "Dr. Reddy’s",
             "Zydus", "Piramal", "Sun Pharma", "Cipla", "Lupin", "Glanbia", "Catalent", "Cambrex",
             "Corbion", "Lycored", "Prinova", "J.B. Chemicals", "Kellogg’s", "Mondelēz", "Cadbury",
             "Teva", "Stauber", "Medifarma", "Isofarma", "Watson", "Tirupati"]

PROCESS = [  # (step, note, photo or None)
    ("Raw material", "Tested raw material and process water enter the reaction.", "hero-warehouse.jpg"),
    ("Reaction", "Raw materials react to form the mineral salt in solution.", "production.jpg"),
    ("Filtration", "The reaction solution is filtered and the residue rejected.", None),
    ("Evaporation", "The clear solution is concentrated; water is removed.", None),
    ("Crystallisation", "The salt crystallises out of the concentrated solution.", None),
    ("Centrifuge", "Crystals are separated from the mother liquor.", "centrifuge.jpg"),
    ("Drying", "Wet cake is dried in a fluid bed dryer.", "fbd.jpg"),
    ("Milling", "Dried material is milled to size.", None),
    ("Homogenisation", "The batch is blended to a uniform lot.", "hero-blending.jpg"),
    ("Sifting", "Powder is sifted to the required mesh.", "sifter.jpg"),
    ("Packing", "Packed after QC approval of the batch.", None),
    ("Dispatch", "Released stock leaves for customers in India and abroad.", None),
]

# ---------------------------------------------------------------- home hero slider
# Full-width slides. Use landscape images at least 2560 x 1280 px for sharp
# results on large screens (see images/hero/AI-PROMPTS.md). Images are cropped
# to fill, never stretched. "pos" sets which part of the photo stays in view.
HERO_SLIDES = [
    ("hero/slide-1-plant.jpg", "Plant II, Mujpur", "Shanpar Plant II building at Mujpur, Vadodara", "70% 45%"),
    ("hero/slide-2-warehouse.jpg", "Raw material store", "Warehouse with palletised raw materials", "50% 60%"),
    ("hero/slide-4-sifting.jpg", "Sifting room", "Clean processing room with a vibro sifter", "60% 55%"),
    ("hero/slide-5-blending.jpg", "Blending room", "Stainless steel blender in a clean room", "50% 50%"),
    ("hero/slide-3-store.jpg", "Finished goods store", "Packed finished goods ready for dispatch", "55% 60%"),
]
