module.exports = {
  extends: [
    'stylelint-config-standard-scss',
    'stylelint-config-prettier-scss',
  ],
  ignoreFiles: [
    'node_modules/**/*',
    'src/static/dist/**/*',
    'ui-system/scss/_tokens.scss',
  ],
  rules: {
    'color-no-hex': true,
    'function-disallowed-list': ['rgb', 'rgba', 'hsl', 'hsla'],
    'no-descending-specificity': null,
    'value-keyword-case': null,
    'selector-class-pattern': [
      '^([a-z0-9]+(?:-[a-z0-9]+)*(?:__(?:[a-z0-9]+(?:-[a-z0-9]+)*))?(?:--[a-z0-9]+(?:-[a-z0-9]+)*)?)$',
      {
        resolveNestedSelectors: true,
        message: 'Use kebab/BEM syntax for class selectors',
      },
    ],
    'scss/load-no-partial-leading-underscore': null,
    'scss/load-partial-extension': null,
    'media-feature-range-notation': null,
    'property-no-vendor-prefix': null,
    'selector-not-notation': null,
    'declaration-empty-line-before': null,
    'rule-empty-line-before': null,
    'declaration-block-single-line-max-declarations': null,
  },
};
