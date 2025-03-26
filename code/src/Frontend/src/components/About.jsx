import { Link } from "react-router-dom";

const About = () => {
  return (
    <div className="min-h-screen bg-gray-900 text-white flex flex-col items-center justify-center">
      {/* Header */}
      <div className="absolute top-4 left-6 text-2xl font-bold">
      </div>

      {/* Main Content */}
      <h2 className="text-4xl font-bold">What is RiskGPT</h2>
      <p className="mt-4 text-lg text-gray-400">
        RiskGPT is an AI-driven platform designed to analyze entity risk using
                advanced machine learning algorithms. Our system evaluates various data
                points to provide intelligent risk assessments.


                <div className="mt-8 text-left max-w-lg">
                                  <h2 className="text-2xl font-semibold mb-3">Contributors</h2>
                                  <ul className="space-y-5">
                                    <li className="flex items-center gap-3"> <strong>Aakriti Saraogi</strong>
                                    </li>
                                    <li className="flex items-center gap-3"> <strong>Samyak Bakliwal</strong>
                                    </li>
                                    <li className="flex items-center gap-3"> <strong>Atharva Marathe</strong>
                                                                        </li>
                                                                        <li className="flex items-center gap-3"> <strong>Wandari Blah</strong>
                                                                                                            </li>

                                  </ul>
                                </div>
      </p>
    </div>
  );
};

export default About;
