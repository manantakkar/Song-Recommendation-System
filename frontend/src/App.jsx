import Home from "./pages/home";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import RecommendationForm from "./pages/home/components/recommendationForm";
import RecommendationByUrl from "./pages/home/components/recommendationByUrl";
const route = createBrowserRouter([
  {
    path: "",
    element: <Home />,
    children: [
      {
        path: "/",
        element: <RecommendationForm />,
      },
      {
        path: "url",
        element: <RecommendationByUrl />,
      },
    ],
  },
]);

function App() {
  return <RouterProvider router={route} />;
}

export default App;
