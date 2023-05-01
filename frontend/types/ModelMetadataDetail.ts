import {BaseInput} from './Input';

export default interface ModelMetadataDetail {
  id: string;
  name: string;
  version: string;
  description: string;
  createdAt: number;
  updatedAt: number;
  inputs: BaseInput[];
}