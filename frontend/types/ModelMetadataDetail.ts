import {BaseInput} from './Input';
import ModelMetadata from './ModelMetadata';

export default interface ModelMetadataDetail extends ModelMetadata {
  inputs: BaseInput[];
}