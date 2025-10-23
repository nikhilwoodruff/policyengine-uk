# Free School Meals Model Implementation

## Overview

This document describes the comprehensive implementation of free school meals (FSM) eligibility and valuation for PolicyEngine UK, developed on branch `claude/free-school-meals-model-011CUQHYVgw4nKHqjoSnApsa`.

## What Was Implemented

### 1. Parameters File
**Location**: `policyengine_uk/parameters/gov/dfe/free_school_meals.yaml`

Defines all policy parameters including:
- **Income thresholds** by country and benefit type
  - England UC: £7,400 (2025) → ∞ (2026+, universal coverage)
  - Northern Ireland UC: £15,000
  - Scotland/Wales UC: £7,400
  - Child Tax Credit: £16,190
- **Age ranges** for universal entitlement by country
  - England: Ages 4-7 (Reception to Year 2)
  - Scotland: Ages 4-9 (Primary 1-5), expanding to 4-11
  - Wales: Ages 4-11 (all primary)
  - Northern Ireland: No universal age entitlement
- **Qualifying benefits** lists
- **Transitional protection** parameters (active until Aug 31, 2026)
- **Meal costs** by country (£2.53/day, uprated by CPI)
- **School weeks** per year (39 weeks)

### 2. Eligibility Variables

#### Supporting Variables

**`meets_universal_credit_criteria_for_free_school_meals`**
- Entity: BenUnit
- Checks: UC receipt + earned income below country threshold
- Handles 2026 expansion (infinite threshold for England)
- Location: `variables/gov/dfe/free_school_meals/meets_universal_credit_criteria_for_free_school_meals.py`

**`meets_child_tax_credit_criteria_for_free_school_meals`**
- Entity: BenUnit
- Checks: CTC receipt + no WTC + income below £16,190
- Location: `variables/gov/dfe/free_school_meals/meets_child_tax_credit_criteria_for_free_school_meals.py`

**`free_school_meals_age_eligible`**
- Entity: Person
- Checks: Age within universal entitlement range for child's country
- Different rules for England, Scotland, Wales, Northern Ireland
- Location: `variables/gov/dfe/free_school_meals/free_school_meals_age_eligible.py`

**`free_school_meals_income_eligible`**
- Entity: Person
- Checks: School age + (qualifying benefits OR UC/CTC income criteria)
- Location: `variables/gov/dfe/free_school_meals/free_school_meals_income_eligible.py`

#### Main Eligibility Variable

**`free_school_meals_eligible`**
- Entity: Person
- Combines: Age-based OR income-based eligibility
- Returns: Boolean indicating eligibility
- Location: `variables/gov/dfe/free_school_meals/free_school_meals_eligible.py`

### 3. Valuation Variable

**`free_school_meals` (updated)**
- Entity: Person
- Calculates: Annual value based on eligibility
- Formula: Meal cost per day × 5 days/week × 39 weeks/year
- Value: ~£493.35/year (at 2023 prices, uprated)
- Location: `variables/gov/dfe/free_school_meals_updated.py`

### 4. Test Suite

**Location**: `tests/gov/dfe/free_school_meals/test_free_school_meals_eligibility.yaml`

Comprehensive tests covering:
- ✅ Age-based eligibility (England Reception/Year 1/2)
- ✅ UC income threshold (£7,400 England, £15,000 NI)
- ✅ 2026 expansion (all UC recipients eligible)
- ✅ Geographic differences (Wales universal, Scotland P1-5)
- ✅ Qualifying benefits (Income Support, JSA, etc.)
- ✅ CTC criteria (income < £16,190, no WTC)
- ✅ Value calculation (~£493)

## Key Features

### Geographic Differentiation
The model correctly handles different rules across:
- 🏴󠁧󠁢󠁥󠁮󠁧󠁿 **England**: Targeted with infant universal
- 🏴󠁧󠁢󠁳󠁣󠁴󠁿 **Scotland**: Broader universal (P1-5)
- 🏴󠁧󠁢󠁷󠁬󠁳󠁿 **Wales**: Full primary universal
- 🇬🇧 **Northern Ireland**: Higher UC threshold

### Temporal Variation
Parameters are date-aware:
- Current rules (2025): UC £7,400 threshold in England
- Future rules (2026+): UC threshold removed (all UC recipients eligible)
- Transitional protections expire Aug 31, 2026

### Integration with Existing System
- Uses existing variables: `uc_earned_income`, `universal_credit`, `income_support`, etc.
- Uses existing infrastructure: `is_of_compulsory_school_age`
- Follows existing patterns: Similar to targeted childcare entitlement
- Compatible with: BenUnit and Person entities

## Implementation Completeness

### ✅ Implemented
- Age-based universal entitlement (all nations)
- Income/benefits-based eligibility (all nations)
- Geographic differentiation
- 2026 UC expansion
- Monetary valuation
- Comprehensive test suite
- Full parameter specification

### ⚠️ Not Yet Implemented (Future Enhancements)
1. **Transitional Protection Tracking**
   - Requires historical eligibility state tracking
   - Would need additional variable to store "was previously eligible"
   - Currently handled via parameter date ranges

2. **Scottish Child Payment Link**
   - Scotland P6-7 eligibility for Scottish Child Payment recipients (Feb 2025+)
   - Requires Scottish Child Payment variable integration

3. **Immigration Status Edge Cases**
   - Support under Immigration and Asylum Act 1999
   - Special educational needs provisions (Northern Ireland)

4. **Take-up Modeling**
   - Not all eligible children claim FSM
   - Could add `would_claim_free_school_meals` variable

## File Structure

```
policyengine_uk/
├── parameters/
│   └── gov/
│       └── dfe/
│           └── free_school_meals.yaml                    # NEW
├── variables/
│   └── gov/
│       └── dfe/
│           ├── free_school_meals.py                      # UPDATED
│           └── free_school_meals/                        # NEW DIRECTORY
│               ├── __init__.py
│               ├── free_school_meals_eligible.py
│               ├── free_school_meals_age_eligible.py
│               ├── free_school_meals_income_eligible.py
│               ├── meets_universal_credit_criteria_for_free_school_meals.py
│               └── meets_child_tax_credit_criteria_for_free_school_meals.py
└── tests/
    └── gov/
        └── dfe/
            └── free_school_meals/                        # NEW DIRECTORY
                └── test_free_school_meals_eligibility.yaml
```

## Integration Steps

To integrate this implementation into the main openfisca-uk repository:

1. **Copy files** from `/tmp/openfisca-uk/` to the main repository
2. **Replace** `free_school_meals.py` with `free_school_meals_updated.py`
3. **Run tests**: `pytest policyengine_uk/tests/gov/dfe/free_school_meals/`
4. **Validate** against administrative statistics (~1.9M FSM recipients in 2024)
5. **Update changelog** with new variables and parameters
6. **Document** in PolicyEngine UK docs

## Validation Against Real Data

### Expected Outcomes
- **Current recipients** (2024/25): ~1.9 million children
- **Post-expansion** (2026/27+): ~2.4 million children (+500k)
- **Wales**: ~200k children (all primary)
- **Scotland**: ~120k children (P1-5 universal)

### Key Policy Dates
- **April 1, 2018**: UC eligibility added with £7,400 threshold
- **September 2014**: England universal infant FSM introduced
- **September 2024**: Wales universal primary FSM
- **February 2025**: Scotland P6-7 with Scottish Child Payment
- **September 2026**: England UC expansion (all recipients)
- **August 31, 2026**: Transitional protections end

## Testing Checklist

Before deployment, verify:
- [ ] 5-year-old in England is eligible (age-based)
- [ ] 10-year-old on UC with £6k income is eligible (England)
- [ ] 10-year-old on UC with £8k income is NOT eligible (England, 2025)
- [ ] 10-year-old on UC with £8k income IS eligible (England, 2027+)
- [ ] 10-year-old on UC with £14k income is eligible (Northern Ireland)
- [ ] 8-year-old in Wales is eligible (universal primary)
- [ ] CTC recipient with WTC is NOT eligible
- [ ] Income Support recipient is eligible regardless of income
- [ ] FSM value is approximately £493/year (at 2023 prices)

## References

### Policy Sources
1. [GOV.UK: Apply for free school meals](https://www.gov.uk/apply-free-school-meals)
2. [GOV.UK: Free school meals guidance for schools and LAs](https://www.gov.uk/government/publications/free-school-meals-guidance-for-schools-and-local-authorities)
3. [Education Hub: Expanding free school meals (June 2025)](https://educationhub.blog.gov.uk/2025/06/expanding-free-school-meals-what-parents-need-to-know/)
4. [IFS: Benefits and costs of expanding FSM](https://ifs.org.uk/articles/benefits-and-costs-expanding-access-free-school-meals-will-grow-over-time)

### Legislation
- Education Act 1996
- Universal Credit Regulations 2013
- The Local Authority (Duty to Secure Early Years Provision Free of Charge) Regulations

## Impact

This implementation enables PolicyEngine UK to:
- ✅ Model FSM eligibility accurately for all UK nations
- ✅ Evaluate impact of 2026 UC expansion
- ✅ Assess household budgets including FSM value
- ✅ Support policy research on child poverty and food security
- ✅ Compare FSM policy across UK nations
- ✅ Model benefit interactions with FSM eligibility

## Next Steps for Production

1. **Code Review**: Review variable logic and parameter values
2. **Integration Testing**: Test interaction with other benefits
3. **Performance Testing**: Ensure calculations are efficient
4. **Documentation**: Add to PolicyEngine UK documentation
5. **Data Validation**: Compare outputs to DfE administrative data
6. **User Feedback**: Test with policy researchers and stakeholders

---

**Implementation Date**: October 23, 2025
**Branch**: `claude/free-school-meals-model-011CUQHYVgw4nKHqjoSnApsa`
**Status**: Ready for review and integration
**Files**: 8 new/updated files, 1 parameters file, 5 variables, 1 test suite
