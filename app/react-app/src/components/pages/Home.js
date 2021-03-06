import "../../styles/Home.css";
import { Container, Row, Col, Button } from "react-bootstrap";
import HomeImg from "../components/HomeImg"

const Home = ({ homeIntro, websiteIMGs }) => {
  return (
    <div>
      <div class="home-top-section padding-5-lr">
        <p class="home-intro">{homeIntro}</p>
      </div>
      <hr />
      <Container className="home-central-container">
        <Row className="home-central-info-row">
          <Col lg={9} className="home-central-info-col">
            {/* <MacImg websiteIMG={websiteIMGs.mac} />
            <IpadImg websiteIMG={websiteIMGs.ipad} />
            <PhoneImg websiteIMG={websiteIMGs.phone} /> */}
            <HomeImg/>
          </Col>
          <Col lg={3} className="home-central-info-col">
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
