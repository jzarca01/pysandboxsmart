# pysandboxsmart

An API for the home roaster [Sandbox Smart](https://www.sandboxsmart.com).

## Installation

In a virtual environment run the following command:

`pip install -r requirements.txt`

## How to use

`fastapi dev src/main.py`

## JSON Schema for a roasting profile

```js
type: 'object',
properties: {
    profile: {
    type: 'object',
    properties: {
        ownerId: { type: 'string' },
        profileId: { type: 'string' },
        profileName: { type: 'string' },
        profileRole: { type: 'string' },
        structType: { type: 'string' },
        structVersion: { type: 'integer' },
        revision: { type: 'integer' },
        createDate: { type: 'string', format: 'date-time' },
        updateDate: { type: 'string', format: 'date-time' },
        supportModel: { type: 'string' },
        supportVoltage: { type: 'string' },
        rawBeanWeight: { type: 'integer' },
        expectedResult: {
        type: 'object',
        properties: {
            roastDegreeShell: { type: 'integer' },
            roastDegreeKernel: { type: 'integer' },
            flavor: { type: 'string' }
        },
        required: ['roastDegreeShell', 'roastDegreeKernel', 'flavor']
        },
        data: {
        type: 'object',
        properties: {
            preHeat: {
            type: 'object',
            properties: {
                temperature: { type: 'integer' },
                continuousTime: { type: 'integer' }
            },
            required: ['temperature', 'continuousTime']
            },
            beanWeight: { type: 'integer' },
            roastLevel: { type: 'string' },
            crackConfig: {
            type: 'object',
            properties: {
                fanSpeed: { type: 'integer' },
                timeline: { type: 'integer' },
                doorAngle: { type: 'integer' },
                drumSpeed: { type: 'integer' },
                heatPower: { type: 'integer' },
                temperature: { type: 'integer' },
                continuousTime: { type: 'integer' }
            },
            required: ['fanSpeed', 'timeline', 'doorAngle', 'drumSpeed', 'heatPower', 'temperature', 'continuousTime']
            },
            crackConfig2: {
            type: 'object',
            properties: {
                fanSpeed: { type: 'integer' },
                timeline: { type: 'integer' },
                doorAngle: { type: 'integer' },
                drumSpeed: { type: 'integer' },
                heatPower: { type: 'integer' },
                temperature: { type: 'integer' },
                continuousTime: { type: 'integer' }
            },
            required: ['fanSpeed', 'timeline', 'doorAngle', 'drumSpeed', 'heatPower', 'temperature', 'continuousTime']
            },
            plannedHeats: {
            type: 'array',
            items: {
                type: 'object',
                properties: {
                fanSpeed: { type: 'integer' },
                timeline: { type: 'integer' },
                doorAngle: { type: 'integer' },
                drumSpeed: { type: 'integer' },
                heatPower: { type: 'integer' },
                temperature: { type: 'integer' },
                continuousTime: { type: 'integer' }
                },
                required: ['fanSpeed', 'timeline', 'doorAngle', 'drumSpeed', 'heatPower', 'temperature', 'continuousTime']
            }
            },
            roomTemperature: { type: 'integer' },
            relativeHumidity: { type: 'integer' }
        },
        required: ['preHeat', 'beanWeight', 'roastLevel', 'crackConfig', 'crackConfig2', 'plannedHeats', 'roomTemperature', 'relativeHumidity']
        },
        coffeeRawBean: {
        type: 'object',
        properties: {
            region: { type: 'string' },
            country: { type: 'string' },
            process: { type: 'string' },
            altitude: { type: 'string' },
            variety: { type: 'string' },
            level: { type: 'string' },
            flavor: { type: 'string' }
        },
        required: ['region', 'country', 'process', 'altitude', 'variety', 'level', 'flavor']
        },
        localeDictionary: {
        type: 'object',
        properties: {
            profileName: {
            type: 'object',
            patternProperties: {
                "^[a-z]{2}_[A-Z]{2}$": { type: 'string' }
            },
            additionalProperties: false
            }
        },
        required: ['profileName']
        }
    },
    required: ['ownerId', 'profileId', 'profileName', 'profileRole', 'structType', 'structVersion', 'revision', 'createDate', 'updateDate', 'supportModel', 'supportVoltage', 'rawBeanWeight', 'expectedResult', 'data', 'coffeeRawBean', 'localeDictionary']
    }
}
```

## Roasting profile documentation

A coffee roasting profile is a set of instructions and parameters that a coffee roaster follows to achieve a specific flavor and quality in the roasted coffee beans. It's like a recipe, but for roasting coffee.

### Key Components of a Roasting Profile

#### 1. Basic Information

- **Profile Name**: The name of the roasting profile, often including the year and ranking in a competition.
- **Creation and Update Dates**: When the profile was created and last modified.
- **Roaster Model**: The specific coffee roasting machine this profile is designed for.

#### 2. Coffee Bean Information

- **Raw Bean Weight**: How much unroasted coffee is being used (usually in grams).
- **Bean Origin**: Where the coffee beans come from, including the country and region.
- **Processing Method**: How the coffee cherries were processed (e.g., washed, natural).
- **Altitude**: How high the coffee was grown, which affects its flavor.

#### 3. Roasting Goals

- **Expected Roast Degree**: How dark the roast should be, both for the outside (shell) and inside (kernel) of the bean.
- **Target Flavor**: The general flavor profile the roaster is aiming for.

#### 4. Roasting Process

- **Preheat**: How hot the roaster should be before adding the coffee beans.
- **Planned Heat Stages**: A series of steps detailing how to adjust the roaster's settings throughout the process, including:
  - Fan Speed: How fast the fan is blowing to control airflow.
  - Drum Speed: How fast the drum holding the beans is rotating.
  - Heat Power: How much heat is being applied.
  - Duration: How long each stage lasts.

#### 5. Crack Configurations

- Settings for when the beans start to "crack" (make popping sounds), which is a crucial point in the roasting process.

#### 6. Environmental Factors

- Room Temperature and Humidity: These can affect the roasting process and are noted to ensure consistency.

#### 7. Translations

- The profile name translated into multiple languages for international use.

### Why are these Profiles Important?

1. **Consistency**: They allow roasters to replicate award-winning roasts consistently.
2. **Learning**: New roasters can study these profiles to understand what makes a great roast.
3. **Competition**: These profiles represent some of the best techniques in coffee roasting competitions.
4. **Customization**: Experienced roasters can use these as a starting point and adjust them for different beans or desired flavors.
