;; ==============================================================================
;; agri-pln-metta: Unified Agricultural Knowledge Base Module
;; ==============================================================================
;; Aggregates all domain knowledge submodules (crops, diseases, symptoms,
;; conditions, treatments) into a single cohesive, interconnected AtomSpace.
;; ==============================================================================

!(import! &self crops)
!(import! &self diseases)
!(import! &self symptoms)
!(import! &self conditions)
!(import! &self treatments)

;; Helper functions to query the unified knowledge base
(= (get-disease-causes $disease)
   (match &self (Relation causes $disease $symptom $tv) ($disease causes $symptom $tv)))

(= (get-symptom-causes $symptom)
   (match &self (Relation causes $disease $symptom $tv) ($disease causes $symptom $tv)))

(= (get-condition-risks $condition)
   (match &self (Relation increases-risk $condition $disease $tv) ($condition increases-risk $disease $tv)))

(= (get-crop-susceptibility $crop)
   (match &self (Susceptible $crop $disease $tv) ($crop susceptible-to $disease $tv)))

(= (get-disease-treatments $disease)
   (match &self (Relation effective-treatment $treatment $disease $tv) ($treatment effective-for $disease $tv)))

(= (get-condition-promoters $cond)
   (match &self (Relation promotes $c1 $cond $tv) ($c1 promotes $cond $tv)))
