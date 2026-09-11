const corsconfig = {
  origin: process.env.CORS_ORIGIN,
  methods: ['GET', 'HEAD', 'POST', 'PUT', 'PATCH', 'DELETE'],
  preflightContinue: false,
  optionsSuccessStatus: 204,
  maxAge: 600, // 10 minutes
  credentials: true,
};

export default corsconfig;