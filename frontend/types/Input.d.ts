export enum InputType {
  LONG_TEXT = 'longText',
  SHORT_TEXT = 'shortText',
  NUMBER = 'number',
}

interface BaseInput {
  id: string;
  fieldName: string;
  type: InputType;
}

interface LongTextInput extends BaseInput {
  type: InputType.LONG_TEXT;
}

interface ShortTextInput extends BaseInput {
  type: InputType.SHORT_TEXT;
}

interface NumberInput extends BaseInput {
  type: InputType.NUMBER;
}
