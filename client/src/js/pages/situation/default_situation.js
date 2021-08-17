export const DEFAULT_HOUSEHOLD = {
	region: {
		title: "Region",
		description: "The region of the UK that this household resides in.",
		default: "South East",
		value: "South East",
		type: "category",
		options: [
			"South East",
			"London",
			"Scotland",
			"North West",
			"East of England",
			"West Midlands",
			"South West",
			"Yorkshire and the Humber",
			"East Midlands",
			"North East",
		]
	}
};

export const DEFAULT_FAMILY = {
	claims_UC: {
		title: "UC claimant",
		description: "Whether this family would claim Universal Credit",
		default: true,
		value: true,
		type: "bool"
	},
	claims_child_benefit: {
		title: "CB claimant",
		description: "Whether this family would claim the Child Benefit",
		default: true,
		value: true,
		type: "bool"
	}
};

export const DEFAULT_ADULT = {
	age: {
		title: "Age",
		description: "The age of the person",
		default: 18,
		value: 18,
		min: 18,
		max: 80
	},
	employment_income: {
		title: "Employment income",
		description: "Income from employment (gross)",
		default: 0,
		value: 0,
		max: 80000
	},
	pension_income: {
		title: "Pension income",
		description: "Income from pensions (excluding the State Pension)",
		default: 0,
		value: 0,
		max: 150000
	},
	savings_interest_income: {
		title: "Savings interest income",
		description: "Income from savings interest (including ISAs)",
		default: 0,
		value: 0,
		max: 5000
	},
	dividend_income: {
		title: "Dividend income",
		description: "Income from dividends",
		default: 0,
		value: 0,
		max: 5000
	},
};

export const DEFAULT_CHILD = {
	age: {
		title: "Age",
		description: "The age of the person",
		default: 10,
		value: 10,
		min: 0,
		max: 17
	},
	employment_income: {
		title: "Employment income",
		description: "Income from employment (gross)",
		default: 0,
		value: 0,
		max: 80000
	},
};

const DEFAULT_SITUATION = {
	household: JSON.parse(JSON.stringify(DEFAULT_HOUSEHOLD)),
	families: {
		"family_1": {
			...JSON.parse(JSON.stringify(DEFAULT_FAMILY)),
		}
	},
	people: {
		"head": JSON.parse(JSON.stringify(DEFAULT_ADULT))
	}
};

export default DEFAULT_SITUATION;