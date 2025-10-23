# Free School Meals Model Investigation

## Executive Summary

This investigation examines the current state of free school meals (FSM) modeling in PolicyEngine UK and proposes comprehensive improvements to accurately reflect current policy, transitional protections, and the 2026 expansion.

## Current Implementation Gaps

### 1. Minimal Implementation
- **Location**: `/tmp/openfisca-uk/policyengine_uk/variables/gov/dfe/free_school_meals.py`
- **Status**: Stub only - defines variable but no eligibility logic
- **Missing**: No formula, no parameters, no eligibility calculations

### 2. No Parameters File
- No YAML parameter file defining:
  - Income thresholds (£7,400 for England UC, £15,000 for NI)
  - Qualifying benefits lists
  - Age thresholds for universal entitlement
  - Geographic variations

### 3. No Geographic Differentiation
The four UK nations have significantly different FSM policies:
- **England**: Targeted + universal for infants
- **Scotland**: Universal primary 1-5, expanding to 6-7
- **Wales**: Universal for all primary
- **Northern Ireland**: Different income threshold (£15,000)

### 4. No Transitional Protection Logic
- Transitional protections extended to end of 2025/26 school year
- Not currently modeled

### 5. No 2026 Expansion
- Major policy change: All UC recipients eligible from Sept 2026
- Will benefit ~500,000 additional children

## Policy Requirements by Nation

### England (Current - 2025/26)

#### Universal Entitlement
- Reception, Year 1, Year 2 (approximately ages 4-7)

#### Income-Based Eligibility (Year 3+)
Children eligible if household receives:
- Income Support
- Income-based Jobseeker's Allowance
- Child Tax Credit (with annual gross income ≤ £16,190, without WTC)
- Working Tax Credit run-on (paid for 4 weeks after stopping work)
- Income-related Employment and Support Allowance
- Support under Part VI of the Immigration and Asylum Act 1999
- Guarantee element of State Pension Credit
- **Universal Credit** with household **earned income < £7,400/year** (after tax, excluding benefits)

#### Transitional Protection (Until End 2025/26)
- Households on UC that previously qualified keep FSM eligibility
- Protections regardless of change in circumstances
- Extended from original March 2025 end date

### England (2026/27 Onwards)

#### Major Expansion
- **All children in households receiving Universal Credit** become eligible
- Income threshold removed for UC recipients
- Estimated to benefit ~1.7 million children long-term
- ~500,000 additional children in short run

### Scotland

#### Current Policy
- **Universal FSM**: Primary 1-5 (all children)
- **Primary 6-7**: Eligible if family receives Scottish Child Payment (from Feb 2025)
- Benefits-based criteria similar to England for secondary

### Wales

#### Current Policy
- **Universal FSM for all primary school children** (implemented by Sept 2024)
- Significantly broader than other nations

### Northern Ireland

#### Current Policy
- **Higher UC threshold**: £15,000/year (not £7,400)
- Special provisions for children with:
  - Statement of special educational needs requiring special diet
  - Boarding at special school
- Otherwise similar benefits-based criteria to England

## Technical Implementation Requirements

### 1. Parameters Structure Needed

```yaml
gov.dfe.free_school_meals:
  income_thresholds:
    universal_credit:
      england: £7,400 (2025), removed (2026+)
      northern_ireland: £15,000
    child_tax_credit: £16,190

  universal_entitlement_ages:
    england: [4, 5, 6, 7]  # Reception to Year 2
    scotland: [4-9]  # Primary 1-5
    wales: [4-11]  # All primary

  qualifying_benefits:
    - income_support
    - JSA_income
    - ESA_income
    - pension_credit_guarantee_credit
    - child_tax_credit (with income check)
    - working_tax_credit_run_on
    - universal_credit (with income check)

  transitional_protection:
    end_date: 2026-08-31  # End of 2025/26 school year
```

### 2. Variables Needed

#### Core Eligibility Variables
- `free_school_meals_eligible` - Main eligibility boolean
- `free_school_meals_income_eligible` - Income-based eligibility
- `free_school_meals_age_eligible` - Age-based universal eligibility
- `free_school_meals_transitional_protection` - Protected status
- `is_in_compulsory_education` - Age check (already exists)

#### Supporting Variables
- By nation variants for different rules
- Income comparison logic using `uc_earned_income`
- Benefits receipt checking

### 3. Implementation Pattern

Based on existing DfE programs (e.g., targeted childcare entitlement):
1. **Entity**: Person (individual child eligibility)
2. **Reference period**: YEAR
3. **Geographic checking**: Use `household.country` for nation-specific rules
4. **Income checking**: Use `benunit.uc_earned_income` for UC threshold
5. **Benefits checking**: Use existing benefit variables (universal_credit, income_support, etc.)

### 4. Value Calculation

Current stub only defines variable structure. Need to:
- Add eligibility formula (boolean or count)
- If monetary value needed: Calculate based on:
  - Number of eligible children
  - Weekly cost per meal × school weeks per year
  - Geographic variation in meal costs

## Recommended Implementation Approach

### Phase 1: Parameters (Immediate)
1. Create `free_school_meals.yaml` parameter file
2. Define income thresholds with temporal variation
3. Define age ranges by nation
4. List qualifying benefits

### Phase 2: Core Eligibility (Immediate)
1. Implement age-based eligibility by nation
2. Implement income-based eligibility (pre-2026)
3. Implement benefits-based eligibility
4. Combine eligibility criteria with proper logic

### Phase 3: Transitional Protection (Immediate)
1. Add transitional protection flag variable
2. Check if previously eligible and on UC
3. Maintain eligibility until 2026-08-31

### Phase 4: 2026 Expansion (Immediate with date check)
1. Add expansion logic effective 2026-09-01
2. All UC recipients eligible (remove income check)
3. Ensure smooth transition from protection period

### Phase 5: Testing
1. Create test cases for each nation
2. Test income threshold boundaries (£7,399 vs £7,401)
3. Test transitional protection scenarios
4. Test 2026 expansion cutover
5. Test age boundaries

## Key Policy Sources

1. **GOV.UK Guidance**: Free school meals guidance for schools and local authorities
2. **Education Hub (June 2025)**: Expansion announcement
3. **Local Authority Updates**: Transitional protection extensions
4. **Legislation**:
   - The Local Authority (Duty to Secure Early Years Provision Free of Charge) Regulations
   - Education Act 1996
   - Universal Credit Regulations 2013

## Success Metrics

A successful implementation should:
1. Accurately model eligibility for all 4 UK nations
2. Correctly apply income thresholds (£7,400 England, £15,000 NI)
3. Handle universal entitlement by age and nation
4. Preserve transitional protections through 2025/26
5. Automatically expand eligibility from Sept 2026
6. Match administrative data on FSM recipients (~1.9M currently, ~2.4M post-expansion)

## Next Steps

1. Review this investigation with stakeholders
2. Confirm parameter values and effective dates
3. Begin implementation of parameters file
4. Implement eligibility variables following DfE patterns
5. Create comprehensive test suite
6. Validate against administrative statistics
7. Document in PolicyEngine UK docs

---

**Investigation Date**: October 23, 2025
**Investigator**: Claude Code
**Branch**: `claude/free-school-meals-model-011CUQHYVgw4nKHqjoSnApsa`
