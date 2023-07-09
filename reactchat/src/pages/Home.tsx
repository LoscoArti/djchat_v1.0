// import { Css } from "@mui/icons-material";
import { Box, CssBaseline } from "@mui/material";
import PrimaryAppBar from "./templates/PrimaryAppBar";

const Home = () => {
    return (

        <Box sx={{display: "flex"}}>
        <CssBaseline />
        <PrimaryAppBar />
        </Box>
    );
};
export default Home;