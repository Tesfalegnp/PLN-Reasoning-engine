# Coffee Agriculture Domain & Plant Pathology Ontology

## 1. Domain Overview
This Probabilistic Logic Network (PLN) reasoning system models expert agricultural diagnosis and crop protection management in **Coffee Agriculture (*Coffea arabica*)**. 

Agricultural field management is inherently plagued by **uncertainty**, **partial observations**, **visual symptom ambiguity**, and **conflicting scout reports**. The system models these conditions with native Simple Truth Values $(s, c)$ and formal probabilistic inference.

---

## 2. Agricultural Domain Ontology

The domain is formalized in [coffee_agriculture.metta](file:///home/hope/Projects/pln_engin_project/metta/kb/coffee_agriculture.metta) with explicit MeTTa type signatures:

```metta
(: CoffeePlant Type)
(: Disease Type)
(: Symptom Type)
(: EnvironmentalRisk Type)
(: SoilCondition Type)
(: Treatment Type)
(: Variety Type)
```

### 2.1 Modeled Entities
- **Coffee Plants**:
  - `CoffeePlant01`: Bourbon cultivar plot in high-humidity canopy.
  - `CoffeePlant02`: High-rainfall plot presenting berry damage.
  - `CoffeePlant03`: Leached, acidic soil plot showing foliage discoloration.
  - `CoffeePlant04`: Control plot (healthy/early season monitoring).
- **Varieties / Cultivars**:
  - `ArabicaBourbon`: High-quality traditional cultivar, susceptible to rust.
  - `ArabicaTypica`: High-quality heirloom cultivar, botanically similar to Bourbon.

---

## 3. Modeled Pathologies & Plant Conditions

### 3.1 Coffee Leaf Rust (*Hemileia vastatrix*)
- **Etiology**: Obligate biotrophic basidiomycete fungus attacking coffee foliage.
- **Observed Symptoms**:
  - `OrangeRustPustules`: Bright orange-yellow urediniospore lesions on the abaxial (underside) leaf surface $(s=0.88, c=0.85)$.
  - `YellowLeafChlorosis`: Discolored chlorotic patches surrounding pustules $(s=0.75, c=0.70)$.
  - `PrematureLeafDrop`: Premature defoliation resulting in reduced photosynthetic capacity.
- **Environmental & Microclimate Drivers**:
  - `HighHumidity`: Relative humidity $>80\%$ facilitating spore germination $(s=0.92, c=0.90)$.
  - `DenseShadedCanopy`: Poor air circulation and persistent leaf wetness $(s=0.80, c=0.75)$.
- **Therapeutic & Cultural Management**:
  - `CopperFungicideSpray`: Preventative copper hydroxide/oxychloride application $(s=0.92, c=0.88)$.
  - `CanopyPruning`: Selective vegetative pruning to lower plot humidity and improve airflow $(s=0.85, c=0.80)$.

### 3.2 Coffee Berry Disease (*Colletotrichum kahawae*)
- **Etiology**: Ascomycete fungus infecting green coffee expanding berries.
- **Observed Symptoms**:
  - `DarkBerryLesions`: Sunken, dark brown-to-black necrotic anthracnose spots $(s=0.90, c=0.85)$.
  - `BerryNecrosis`: Advanced berry mummification and premature fruit drop $(s=0.82, c=0.78)$.
- **Environmental Drivers**:
  - `HeavyRainfall`: Rain splash dispersing fungal conidia across branch clusters $(s=0.85, c=0.80)$.
- **Therapeutic Management**:
  - `TargetedBerryFungicide`: Specialized systemic fungicide protocol targeted to pinhead/expanding berries $(s=0.90, c=0.85)$.

### 3.3 Nitrogen Chlorosis / Soil Nutrient Deficiency
- **Etiology**: Abiotic physiological nutrient deficiency due to soil nitrogen depletion or acidic leaching.
- **Observed Symptoms**:
  - `YellowLeafChlorosis`: Generalized uniform pale chlorosis across older leaves $(s=0.85, c=0.80)$.
- **Soil Risk Factors**:
  - `AcidicLeachedSoil`: Sandy, acidic soil with low cation exchange capacity $(s=0.80, c=0.75)$.
- **Therapeutic Management**:
  - `NitrogenFertilizer`: Direct application of urea or ammonium nitrate $(s=0.95, c=0.92)$.

---

## 4. Why Agricultural Reasoning Requires PLN

### 4.1 Multiple Explanations for the Same Symptom
A common symptom such as **Yellow Leaf Chlorosis** can arise from:
1. `CoffeeLeafRust`: Chlorotic halo surrounding fungal sporulation.
2. `NitrogenDeficiency`: Abiotic nutrient deficiency caused by soil leaching.

In classical crisp logic, $Chlorosis \to Rust$ and $Chlorosis \to NitrogenDeficiency$ would yield conflicting or over-certain conclusions. In PLN:
- When only `YellowLeafChlorosis` is present on `CoffeePlant03`, the system does **not** falsely deduce leaf rust ($s=0.0, c=0.0$ proof failure).
- Instead, it proves `(AfflictedWith CoffeePlant03 NitrogenDeficiency)` with its corresponding confidence.

### 4.2 Handling Conflicting Field Scout Observations
Field conditions lead to observer disagreement:
- **Scout A (Senior Field Agronomist)**: Confirms active orange pustules on `CoffeePlant01` $\to (stv\ 0.85\ 0.75)$.
- **Scout B (Junior Field Assistant)**: Inspects upper leaves and reports symptoms absent $\to (stv\ 0.20\ 0.70)$.

Rather than discarding either observation, **PLN Revision** pools the weight of evidence:
$$w_1 = \frac{0.75}{1 - 0.75} = 3.0, \quad w_2 = \frac{0.70}{1 - 0.70} \approx 2.333$$
$$s_{fused} = \frac{0.85 \times 3.0 + 0.20 \times 2.333}{3.0 + 2.333} = 0.5656, \quad c_{fused} = \frac{5.333}{6.333} \approx 0.8421$$
The resulting belief balances both observations, while the confidence **strictly increases** $(0.8421 > 0.75)$, accurately reflecting more total observation samples!

---

## 5. Agronomic Scope & Disclaimer
> **Important Note**: The relationships formalized in `coffee_agriculture.metta` represent simplified demonstration domain knowledge developed for AI knowledge engineering, probabilistic reasoning research, and PLN verification. They are **not** an automated replacement for certified agronomic field pathology inspection or official extension service advice.
