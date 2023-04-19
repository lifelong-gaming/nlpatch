import {Button, Paper, Card, CardHeader, CardContent, Typography, CardActions} from '@mui/material'
import ModelMetadata from "@/types/ModelMetadata";


interface Prop {
  modelMetadata: ModelMetadata;
  onStartDialogue: (id: string) => void;
}
const ModelMetadataCard = (props: Prop) => {
  const { modelMetadata, onStartDialogue } = props;
  return (
    <Paper elevation={3}>
      <Card>
        <CardHeader title={modelMetadata.name} subheader={modelMetadata.version} />
        <CardContent>
          <Typography variant="body1" color="textSecondary" component="p">
            {modelMetadata.description}
          </Typography>
        </CardContent>
        <CardActions>
          <Button onClick={() => {onStartDialogue(modelMetadata.id)}} size="small">Start Dialogue</Button>
        </CardActions>
      </Card>
    </Paper>
  );
};

export default ModelMetadataCard
