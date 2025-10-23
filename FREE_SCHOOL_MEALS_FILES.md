# Free School Meals Implementation Files

This document lists all implementation files created for the free school meals model. These files are located in `/tmp/openfisca-uk/` and need to be integrated into the main PolicyEngine openfisca-uk repository.

## Files Created

### 1. Parameters File
```
/tmp/openfisca-uk/policyengine_uk/parameters/gov/dfe/free_school_meals.yaml
```
Complete parameter specification including:
- Income thresholds by country and time period
- Age ranges for universal entitlement
- Qualifying benefits lists
- Meal costs and school weeks
- Transitional protection parameters

### 2. Variable Files

#### Main Eligibility
```
/tmp/openfisca-uk/policyengine_uk/variables/gov/dfe/free_school_meals/free_school_meals_eligible.py
```
Master eligibility variable combining age-based and income-based criteria.

#### Age-Based Eligibility
```
/tmp/openfisca-uk/policyengine_uk/variables/gov/dfe/free_school_meals/free_school_meals_age_eligible.py
```
Handles universal entitlement by age for England, Scotland, Wales.

#### Income-Based Eligibility
```
/tmp/openfisca-uk/policyengine_uk/variables/gov/dfe/free_school_meals/free_school_meals_income_eligible.py
```
Handles benefits-based and income-threshold eligibility.

#### Universal Credit Criteria
```
/tmp/openfisca-uk/policyengine_uk/variables/gov/dfe/free_school_meals/meets_universal_credit_criteria_for_free_school_meals.py
```
UC-specific income threshold checks by country, with 2026 expansion logic.

#### Child Tax Credit Criteria
```
/tmp/openfisca-uk/policyengine_uk/variables/gov/dfe/free_school_meals/meets_child_tax_credit_criteria_for_free_school_meals.py
```
CTC-specific income threshold checks (£16,190 limit, no WTC).

#### Module Init
```
/tmp/openfisca-uk/policyengine_uk/variables/gov/dfe/free_school_meals/__init__.py
```
Python module initialization for the free_school_meals package.

### 3. Updated Main Variable
```
/tmp/openfisca-uk/policyengine_uk/variables/gov/dfe/free_school_meals_updated.py
```
Updated `free_school_meals` variable with valuation formula.
**Action Required**: Replace existing `free_school_meals.py` with this file.

### 4. Test Suite
```
/tmp/openfisca-uk/policyengine_uk/tests/gov/dfe/free_school_meals/test_free_school_meals_eligibility.yaml
```
Comprehensive YAML test suite with 12 test cases covering:
- Age-based eligibility
- UC income thresholds
- Geographic variations
- 2026 expansion
- Benefit qualifications
- Monetary valuation

## Quick Access Commands

### View All Implementation Files
```bash
# Parameters
cat /tmp/openfisca-uk/policyengine_uk/parameters/gov/dfe/free_school_meals.yaml

# Variables
ls -la /tmp/openfisca-uk/policyengine_uk/variables/gov/dfe/free_school_meals/

# Tests
cat /tmp/openfisca-uk/policyengine_uk/tests/gov/dfe/free_school_meals/test_free_school_meals_eligibility.yaml
```

### Copy Files to Main Repository
```bash
# When ready to integrate into main openfisca-uk repository:

# 1. Copy parameters
cp /tmp/openfisca-uk/policyengine_uk/parameters/gov/dfe/free_school_meals.yaml \
   <openfisca-uk-repo>/policyengine_uk/parameters/gov/dfe/

# 2. Copy variable directory
cp -r /tmp/openfisca-uk/policyengine_uk/variables/gov/dfe/free_school_meals \
   <openfisca-uk-repo>/policyengine_uk/variables/gov/dfe/

# 3. Replace main variable
cp /tmp/openfisca-uk/policyengine_uk/variables/gov/dfe/free_school_meals_updated.py \
   <openfisca-uk-repo>/policyengine_uk/variables/gov/dfe/free_school_meals.py

# 4. Copy tests
mkdir -p <openfisca-uk-repo>/policyengine_uk/tests/gov/dfe/free_school_meals
cp /tmp/openfisca-uk/policyengine_uk/tests/gov/dfe/free_school_meals/test_free_school_meals_eligibility.yaml \
   <openfisca-uk-repo>/policyengine_uk/tests/gov/dfe/free_school_meals/
```

## File Statistics

- **Total Files Created**: 8
- **Parameters Files**: 1
- **Variable Files**: 6 (5 new + 1 updated)
- **Test Files**: 1
- **Lines of Code**: ~600
- **Test Cases**: 12

## Integration Checklist

- [ ] Copy parameters file to openfisca-uk
- [ ] Copy free_school_meals/ variable directory to openfisca-uk
- [ ] Replace main free_school_meals.py variable
- [ ] Copy test suite to openfisca-uk
- [ ] Run test suite: `pytest policyengine_uk/tests/gov/dfe/free_school_meals/`
- [ ] Update CHANGELOG.md
- [ ] Update documentation
- [ ] Validate against administrative data
- [ ] Create pull request

## Dependencies

The implementation uses these existing variables (no changes required):
- `universal_credit`
- `uc_earned_income`
- `income_support`
- `JSA_income`
- `ESA_income`
- `pension_credit_guarantee_credit`
- `child_tax_credit`
- `working_tax_credit`
- `adjusted_net_income`
- `is_of_compulsory_school_age`
- `age`
- `household.country`

## Next Steps

1. **Review** the implementation files
2. **Test** locally in openfisca-uk development environment
3. **Integrate** into main openfisca-uk repository
4. **Deploy** with next PolicyEngine UK release
5. **Monitor** for accuracy against DfE statistics

---

All implementation files are ready and waiting in `/tmp/openfisca-uk/`.
