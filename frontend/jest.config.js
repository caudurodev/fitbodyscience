module.exports = {
    preset: 'ts-jest',
    testEnvironment: 'node',
    moduleFileExtensions: ['ts', 'tsx', 'js', 'jsx', 'json', 'node'],
    transform: {
        '^.+\\.tsx?$': 'ts-jest',
    },
    moduleNameMapper: {
        '^@/(.*)$': '<rootDir>/src/$1',
    },
    transformIgnorePatterns: ['<rootDir>/node_modules/'],
    globals: {
        'ts-jest': {
            diagnostics: {
                ignoreCodes: [2345, 7006, 7031], // Add other TypeScript error codes you want to ignore
            },
        },
    },
};
