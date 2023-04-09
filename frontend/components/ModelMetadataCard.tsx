import {Paper, Card, CardHeader, CardContent, Typography} from '@mui/material'
import ModelMetadata from "@/types/ModelMetadata";


interface Prop {
  modelMetadata: ModelMetadata;
}
const ModelMetadataCard = (props: Prop) => {
  const { modelMetadata } = props;
  return (
    <Paper elevation={3}>
      <Card>
        <CardHeader title={modelMetadata.name} />
        <CardContent>
          <Typography variant="body2" color="textSecondary" component="p">
            {modelMetadata.description}
          </Typography>
        </CardContent>
      </Card>
    </Paper>
  );
};

export default ModelMetadataCard