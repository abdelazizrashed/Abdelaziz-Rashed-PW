import "../../styles/Home.css";
import { Container, Row, Col, Button } from "react-bootstrap";
import MacImg from "../components/MacImg";
import IpadImg from "../components/IpadImg";
import PhoneImg from "../components/PhoneImg";

const Home = (homeIntro) => {
  homeIntro =
    "Freelance Software Developer from Egypt. \nHighly experienced in Full-Stack Web Development, Game Development, and Cross-Platform App Development.";
  return (
    <div>
      <div class="home-top-section padding-5-lr">
        <p class="home-intro">{homeIntro}</p>
      </div>
      <hr />
      <Container className="home-centeral-container">
        <Row className="home-centeral-info-row">
          <Col lg={9} className="home-centeral-info-col">
            <MacImg />
            <IpadImg />
            <PhoneImg />
          </Col>
          <Col lg={3} className="home-centeral-info-col">
            <p className="home-central-text">
              High performance and fully responsive apps and websites.
            </p>
            <Button
              variant="outline-dark"
              className="view-projects-btn"
              href="/projects"
            >
              View Projects <i class="fas fa-chevron-right"></i>
            </Button>
          </Col>
        </Row>
      </Container>
    </div>
  );
};

export default Home;
